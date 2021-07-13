import json
import re
import glob

liste = glob.glob("distances/*/*")

#Output:
# chaque type de dist pour chaque OCR liste dist entre les textes ,  
# chaque type de dist pour chaque OCR et chaque NER liste dist entre entités

dic_out = {}
for path_json in liste:
  with open(path_json) as f:
    dic_in = json.load(f)
  ocr_version = list(dic_in["txt"].keys())[0]
  ocr_version = re.sub("--|PP", "", ocr_version)
  ocr_version = re.sub("Tesserat", "Tesseract", ocr_version)

  for type_file, dic_versions in dic_in.items():
    for ner_version, dic_dist in dic_versions.items():
      models = re.split("--", ner_version)
      for type_dist, l_dist in dic_dist.items():
        dic_out.setdefault(type_dist, {})
        dic_out[type_dist].setdefault(ocr_version, {"txt":[], "json":{}})
        if type_file=="txt":
          dic_out[type_dist][ocr_version][type_file].append(l_dist[0])
        elif  models[0] == models[1]:
          dic_out[type_dist][ocr_version][type_file].setdefault(ner_version, [])
          dic_out[type_dist][ocr_version][type_file][ner_version].append(l_dist[0])
print("Versions OCR dans cet échantillon :")
print(sorted(list(dic_out["jaccard"].keys())))

for ocr_version, dic_version in dic_out["jaccard"].items():
  dist_txt = dic_version["txt"]
  print("  ", ocr_version, len(dist_txt))

from scipy import stats

out_latex = []
for type_dist, dic_dist in dic_out.items():
  first_line = ["Dist."]
  this_line = [type_dist]
  for ocr_version, dic_version in dic_dist.items():
    dist_txt = dic_version["txt"]
    for ner_model, dist_ner in dic_version["json"].items():
      spearman, pValue = stats.spearmanr(dist_txt, dist_ner)
      spearman = round(spearman, 3)
      pValue = round(pValue, 3)
      first_line.append(f"{ocr_version}:{ner_model}")
      this_line.append(f"{spearman} (p={pValue})")
  out_latex.append(this_line)


path_out = "tab_spearman.tex"

with open(path_out, "w") as w:
  w.write("\\begin{tabular}{%s}\n"%("c|"*len(first_line)))
  w.write("&".join(first_line)+"\\\\\n")
  for line in out_latex:
    w.write("&".join(line)+"\\\\\n")
  w.write("\end{tabular}")
print(f"table lines written in {path_out}")

#comme le tableau va mieux dans l'autre sens, on va faire une transposition :
print("Transposition !!")
from numpy import transpose
out_latex_transposed = transpose(out_latex)
print("colonnes : ", out_latex_transposed[0])
first_line_transposed = ["version"] + list(out_latex_transposed[0])
print(out_latex_transposed[1])


path_out = "tab_spearman_transposed.tex"

with open(path_out, "w") as w:
  w.write("\\begin{tabular}{%s}\n"%("c|"*len(first_line_transposed)))
  w.write("&".join(first_line_transposed)+"\\\\\n")
  for cpt, line in enumerate(out_latex_transposed[1:]):#car [0] c'est l'entête
    line = [first_line[cpt+1]]+list(line)
    w.write("&".join(line)+"\\\\\n")
  w.write("\end{tabular}")
print(f"table lines (reversed) written in {path_out}")
