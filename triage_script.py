import os
import shutil
import csv
import re

# Paths
ROOT_DIR = "C:\\Users\\yuri\\OneDrive\\Desktop\\omniroute"
ORIGINALS_DIR = os.path.join(ROOT_DIR, "originais_preservados")
CLEANED_DIR = os.path.join(ROOT_DIR, "dados_limpos")
REMOVED_DIR = os.path.join(ROOT_DIR, "arquivos_removidos")
MANUAL_DIR = os.path.join(ROOT_DIR, "revisao_manual")
REPORT_FILE = os.path.join(ROOT_DIR, "relatorios", "relatorio_triagem.csv")

# Extensions to remove automatically
REMOVE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.mp4', '.avi', '.mov'}

def is_spectral_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [f.readline() for _ in range(20)]
            # Look for lines that look like numeric columns
            numeric_lines = 0
            for line in lines:
                if not line: continue
                # Check if line contains mostly numbers and separators
                parts = line.split()
                if len(parts) >= 2 and all(re.match(r'^-?\d*\.?\d+([eE][-+]?\d+)?$', p.replace(',', '.')) for p in parts[:2]):
                    numeric_lines += 1

            return numeric_lines >= 2 # Require at least 2 numeric lines to be considered data
    except Exception:
        return False

def main():
    # Ensure directories exist
    os.makedirs(CLEANED_DIR, exist_ok=True)
    os.makedirs(REMOVED_DIR, exist_ok=True)
    os.makedirs(MANUAL_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)

    with open(os.path.join(ROOT_DIR, "all_files.txt"), 'r', encoding='utf-8') as f:
        files = [line.strip() for line in f if line.strip()]

    report_data = []

    for rel_path in files:
        abs_path = os.path.join(ROOT_DIR, rel_path)
        # The rel_path in all_files.txt already starts with 'originais_preservados'
        # But let's make sure we are pointing to the right place.
        # The find command used: find originais_preservados/Raman -type f
        # So rel_path is something like 'originais_preservados/Raman/...'

        # Use the absolute path derived from the file list
        actual_abs_path = os.path.abspath(rel_path) # This might be wrong if the list is relative to project root
        # Let's use the path as is if it's already absolute or relative to current dir
        if not os.path.isabs(rel_path):
            actual_abs_path = os.path.join(ROOT_DIR, rel_path)
        else:
            actual_abs_path = rel_path

        if not os.path.exists(actual_abs_path):
            continue

        filename = os.path.basename(actual_abs_path)
        extension = os.path.splitext(filename)[1].lower()

        decision = "mantido"
        reason = "Arquivo de dados Raman válido"
        category = "desconhecida"
        problem = "Nenhum"
        target_dir = CLEANED_DIR

        # 1. Filter by extension
        if extension in REMOVE_EXTENSIONS:
            decision = "removido"
            reason = f"Extensão não permitida ({extension})"
            target_dir = REMOVED_DIR
        elif extension != '.txt' and extension != '.dat' and extension != '.csv':
            # Other extensions go to manual review unless they are known text-like
            decision = "revisao_manual"
            reason = f"Extensão incomum ({extension})"
            target_dir = MANUAL_DIR
        else:
            # 2. Check if it's actually spectral data
            if not is_spectral_data(actual_abs_path):
                decision = "removido"
                reason = "Arquivo de texto sem dados espectrais utilizáveis"
                target_dir = REMOVED_DIR
            else:
                # It's a valid spectral file.
                # Check if it's PL or other technique (hard to do without deep analysis,
                # but we can check for keywords in filename)
                if "pl" in filename.lower() or "luminescence" in filename.lower():
                    decision = "revisao_manual"
                    reason = "Possível dado de fotoluminescência"
                    target_dir = MANUAL_DIR

                # Simple category detection from filename
                fn_lower = filename.lower()
                if "amino" in fn_lower or "arginine" in fn_lower or "alaninato" in fn_lower:
                    category = "aminoacidos"
                elif "perov" in fn_lower:
                    category = "perovskitas"
                elif "nano" in fn_lower or "cnt" in fn_lower:
                    category = "nanotubos"
                else:
                    category = "outras"

        # Record for report
        report_data.append({
            "Nome original": filename,
            "Tipo de arquivo": extension,
            "Tipo de dado identificado": "Espectral" if decision == "mantido" else "Não espectral/Outro",
            "Decisão": decision,
            "Motivo": reason,
            "Categoria": category,
            "Problemas": problem
        })

        # Move file
        try:
            # To avoid name collisions in flat directories, prepend a hash or keep path structure
            # For now, we'll use the original filename but we should be careful.
            # Better: create a unique name if conflict exists.
            dest_path = os.path.join(target_dir, filename)
            if os.path.exists(dest_path):
                # Append a small unique suffix if file exists
                name, ext = os.path.splitext(filename)
                import uuid
                dest_path = os.path.join(target_dir, f"{name}_{uuid.uuid4().hex[:6]}{ext}")

            shutil.copy2(actual_abs_path, dest_path)
        except Exception as e:
            print(f"Error moving {filename}: {e}")

    # Write report
    with open(REPORT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Nome original", "Tipo de arquivo", "Tipo de dado identificado", "Decisão", "Motivo", "Categoria", "Problemas"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(report_data)

    print(f"Triagem concluída. Relatório salvo em {REPORT_FILE}")

if __name__ == "__main__":
    main()
