"""GN: reconciliar gn_p21_check2 (disse invariante) vs gn_p21n_check (disse observavel).

Hipotese do conflito: o metrica "rel = max|dI|/I" e INFLADA por reflexoes com
I ~ 1e-13 (perto de zero), onde o round-off relativo e grande. O teste certo e:
  1) I_t = c * I_0 com c CONSTANTE  (gauge: so uma fase global)
  2) perfil normalizado identico

E o teste do grupo:
  P2_1 (IT #4)  = {E, 2_1}                 -- translacao em b COMUTA -> gauge continuo
  P2_1/n (IT14) = {E, 2_1, i, n}           -- a inversao i troca y -> -y, logo
                                              T_t(i r) != i(T_t r) -> gauge so DISCRETO (t=0, 1/2)
"""
import numpy as np

a, b, c = 9.441, 5.222, 11.337
beta = np.deg2rad(109.00)
A = np.array([[a, 0.0, 0.0], [0.0, b, 0.0], [0.0, c * np.cos(beta), c * np.sin(beta)]])
Ainv = np.linalg.inv(A)

UA = np.array([[0.10, 0.25, 0.10], [0.35, 0.60, 0.40],
               [0.62, 0.15, 0.75], [0.88, 0.85, 0.20]])


def screw(r):
    return np.array([-r[0], r[1] + 0.5, -r[2]])


def inv(r):
    return np.array([-r[0], -r[1], -r[2]])


def n_op(r):
    return np.array([r[0] + 0.5, r[1] + 0.5, r[2]])


def orbitas(ua, ops):
    out = []
    for op in ops:
        for r in ua:
            out.append(op(np.asarray(r, float)))
    out = np.array(out)
    return out - np.floor(out)


def F_calc(frac, hkl):
    G = np.linalg.norm(np.dot(hkl, Ainv))
    f = np.exp(-0.5 * (0.8 * G) ** 2)
    F = 0.0 + 0.0j
    for r in frac:
        F += f * np.exp(2j * np.pi * np.dot(hkl, r))
    return F


H = []
for h in range(0, 5):
    for k in range(-6, 7):
        for l in range(-5, 6):
            if h == 0 and k == 0 and l == 0:
                continue
            H.append((h, k, l))
H = np.array(H, float)

OPS = {
    "P2_1  (IT #4)  {E, 2_1}": [lambda r: r, screw],
    "P2_1/n (IT #14) {E,2_1,i,n}": [lambda r: r, screw, inv, n_op],
}

for rotulo, ops in OPS.items():
    base = orbitas(UA, ops)
    I0 = np.array([np.abs(F_calc(base, h)) ** 2 for h in H])
    print(f"\n================ {rotulo}  ({len(base)} atomos) ================")
    print(f"  I0: max = {I0.max():.6e} | min = {I0.min():.3e} | "
          f"n reflexoes com I < 1e-6 do max = {(I0 < 1e-6 * I0.max()).sum()}")
    for t in [0.0119, 0.0591, 0.1, 0.25, 0.5]:
        ua_t = UA.copy()
        ua_t[:, 1] += t
        ot = orbitas(ua_t, ops)
        It = np.array([np.abs(F_calc(ot, h)) ** 2 for h in H])

        # (a) metrica ingenua: max|dI|/I  (inflada por I~0)
        rel = np.max(np.abs(It - I0) / np.maximum(I0, 1e-30))
        # (b) teste de gauge: It == c*I0 ?
        ratio = It / np.maximum(I0, 1e-300)
        c = np.median(ratio)
        # restringe as reflexoes com I relevante (>= 1e-3 do max) para nao inflar
        mask = I0 > 1e-3 * I0.max()
        c2 = np.median(ratio[mask])
        esc = np.max(np.abs(It[mask] - c2 * I0[mask]) / (c2 * I0[mask]))
        # (c) perfil normalizado (escala livre por reflexao)
        p0 = I0 / I0.max()
        pt = It / It.max()
        esc_p = np.max(np.abs(pt[mask] - p0[mask]) / np.maximum(p0[mask], 1e-30))
        veredito = "GAUGE" if esc < 1e-8 else "OBSERVAVEL"
        print(f"  t={t:6.4f} | max|dI|/I={rel:9.3e} | c={c2:9.6f} | "
              f"max|It-c*I0|/(c*I0)={esc:9.3e} | perfil esc={esc_p:9.3e} -> {veredito}")

    # (d) a translacao da UA gera o MESMO conjunto transladado? (teste puramente geometrico)
    t = 0.0591
    ua_t = UA.copy()
    ua_t[:, 1] += t
    o0 = np.sort(orbitas(UA, ops).ravel())
    ot = np.sort(orbitas(ua_t, ops).ravel())
    desl = ot - o0
    desl = desl - np.round(desl)
    print(f"  [geom] deslocamento do conjunto orbitado por t=0,0591: "
          f"max|desl| fracionario = {np.max(np.abs(desl)):.3e} "
          f"(0 = mesmo conjunto transladado -> gauge)")
