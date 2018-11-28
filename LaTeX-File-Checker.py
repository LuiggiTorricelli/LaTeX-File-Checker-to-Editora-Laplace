# coding: latin-1

import fileinput as f
import re
import io

filename = str(input('Diretório do arquivo: ')).strip()
print('\n')
preamble = """
\\documentclass{article}
\\usepackage[utf8]{inputenc}
\\usepackage[portuguese]{babel}
\\usepackage{amssymb}
\\usepackage{amsmath}
\\usepackage{txfonts}
\\usepackage{mathdots}
\\usepackage[classicReIm]{kpfonts}
\\usepackage{graphicx}
\\usepackage{geometry}
\\geometry{a4paper,left=30mm,top=25mm,bottom=25mm,right=30mm}
\\providecommand{\\sin}{} \\renewcommand{\\sin}{\\hspace{2pt}\\mathrm{sen}}
\\providecommand{\\tan}{} \\renewcommand{\\tan}{\\hspace{2pt}\\mathrm{tg}}
\\providecommand{\\arcsin}{} \\renewcommand{\\arcsin}{\\hspace{2pt}\\mathrm{arcsen}}
\\providecommand{\\arctan}{} \\renewcommand{\\arctan}{\\hspace{2pt}\\mathrm{arctg}}
\\providecommand{\\csc}{} \\renewcommand{\\csc}{\\hspace{2pt}\\mathrm{cossec}}
\\providecommand{\\cot}{} \\renewcommand{\\cot}{\\hspace{2pt}\\mathrm{cotg}}
\\providecommand{\\sinh}{} \\renewcommand{\\sinh}{\\hspace{2pt}\\mathrm{senh}}
\\providecommand{\\tanh}{} \\renewcommand{\\tanh}{\\hspace{2pt}\\mathrm{tgh}}
\\providecommand{\\coth}{} \\renewcommand{\\coth}{\\hspace{2pt}\\mathrm{cotgh}}
\\usepackage{calc}
\\usepackage[scaled]{helvet}
\\renewcommand\\familydefault{\\sfdefault}
\\usepackage[T1]{fontenc}
\\usepackage[table]{xcolor}
\\usepackage{multirow}
\\usepackage{array}
\\renewcommand{\\lim}{\\mathop{\\mathrm{lim}}\\limits}
\\let\\oldsum\\sum
\\renewcommand{\\sum}{\\displaystyle\\oldsum\\limits}
\\newcommand{\\questao}[1]{\\ignorespaces}
\\newcommand{\\alternativas}[1]{\\ignorespaces}
\\newcommand{\\resolucao}[1]{\\ignorespaces}
\\newcommand{\\resposta}[1]{\\ignorespaces}
\\newcommand{\\compartilhado}[1]{\\ignorespaces}
\\newcommand{\\fimcompartilhado}[1]{\\ignorespaces}
\\setlength\\parindent{0cm}
\\renewcommand{\\baselinestretch}{1.25}
"""

with open(filename, 'r+') as antes, open(filename[:-4] + '.CORRIGIDO.tex', 'w') as depois:
    conteudo = antes.read()
    removePreamble = re.sub(r'.*[\s\S]+(?=\\begin{document})', '', conteudo, 1)
    noIndent = re.sub(r'\\noindent[ ]*', '', removePreamble)
    removeSpaces = noIndent.replace('\n\n\n\n', '\n\n\\text{}\\\\\n\n')
    changeEqref = re.sub(r"\\eqref{GrindEQ__([0-9]+)_}", r"(\1)", removeSpaces)
    changeRef = re.sub(r"\\ref{GrindEQ__([0-9]+)_}", r"(\1)", changeEqref)
    changeKeywords = changeRef.replace("sublinhado", "destacado").replace("sublinhados", "destacados").replace("sublinhada", "destacada").replace("sublinhadas", "destacadas").replace("grifado", "destacado").replace("grifados", "destacados").replace("grifada", "destacada").replace("grifadas", "destacadas")
    changeAccent = changeKeywords.replace("\`{a}", "à").replace("\\'{a}", "á").replace("\\'{e}", "é").replace('\`{e}', 'è').replace("\\'{i}", "í").replace("\\'{o}", "ó").replace("\\'{u}", "ú").replace("\\^{a}", "â").replace("\\^{e}", "ê").replace("\\^{o}", "ô").replace("\\^{u}", "û").replace("\\c{c}", "ç").replace("\\~{a}", "ã").replace("\\~{o}", "õ").replace("\\`{A}", "À").replace("\\'{A}", "Á").replace("\\'{E}", "É").replace("\\'{I}", "Í").replace("\\'{O}", "Ó").replace("\\'{U}", "Ú").replace("\\^{A}", "Â").replace("\\^{E}", "Ê").replace("\\^{O}", "Ô").replace("\\^{U}", "Û").replace("\\c{C}", "Ç").replace("\\~{A}", "Ã").replace("\\~{O}", "Õ")
    upperQuestion = changeAccent.replace("{Questão", "{QUESTÃO")
    fixQuestionName = upperQuestion.replace("{QUESTÃO n$\\boldsymbol{{}^\\circ}$", "{QUESTÃO")
    fixQuestionSpacesMultD = re.sub(r"\\textbf{\\underbar{QUESTÃO ([0-9]+)[ ]*}}", r"\\textbf{QUESTÃO \1}", fixQuestionName)
    fixQuestionNumber = re.sub(r"\\textbf{QUESTÃO ([0-9])}", r"\\textbf{QUESTÃO 0\1}", fixQuestionSpacesMultD)
    estabilishQuestion = re.sub(r"\\textbf{QUESTÃO ([0-9]+)}", r"\\questao{\1}\n\\textbf{QUESTÃO \1}", fixQuestionNumber)
    fixQuestion = re.sub(r"\\questao{0([0-9]+)}", r"\\questao{\1}", estabilishQuestion)
    changeUnderbar = fixQuestion.replace("\\underbar", "\\textbf")
    fixTimes = changeUnderbar.replace('\\ \\times \\', ' \\times ')
    fixDegrees = fixTimes.replace('\\mathtt{{}^\\circ\\!{C}}','^\\circ\\text{C}')
    fixMathrmDelta = fixDegrees.replace('\\mathrm{\\Delta }', '\\Delta ')
    fixMathrmFunctions = fixMathrmDelta.replace("\\mathrm{sen}", "\\sin").replace("\\mathrm{tg}", "\\tan").replace("\\mathrm{log}", "\\log").replace("\\mathrm{cos}", "\\cos").replace("\\mathrm{lim}", "\\lim").replace("\\mathrm{cossec}", "\\csc").replace("\\mathrm{arctg}", "\\arctan").replace("\\mathrm{arcsen}", "\\arcsin").replace("\\mathrm{cotg}", "\\cot").replace("\\mathrm{senh}", "\\sinh").replace("\\mathrm{cotgh}", "\\coth").replace("\\mathrm{tgh}", "\\tanh")
    fixMathrmGeneral = re.sub(r"\\mathrm{([^}]*)}", r"\1", fixMathrmFunctions)
    fixMeasureUnits = fixMathrmGeneral.replace('\\ N/m^2$', '\\ \\text{N/m}^2$').replace('\\ cm$', '\\ \\text{cm}$')
    regexUniqueMeasureUnit = re.sub(r"([0-9]+)\\ ([A-z])\$", r"\1\\ \\text{\2}$", fixMeasureUnits)
    changeMathDelimiters = regexUniqueMeasureUnit.replace('\\[', '$$').replace('\\]', '$$').replace('\\(', '$').replace('\\)', '$')
    changeBoxedOne = re.sub(r"\\left\|\\! {\\overline{{\\underline{([^}]+)}} }}  \\!\\right\|", r"\\boxed{\1}", changeMathDelimiters)
    changeBoxedTwo = re.sub(r"\\underline{\\overline{\\left\|([^|]+)\\right\|}}", r"\\boxed{\1}", changeBoxedOne)
    fixKernNulldelimiter1 = re.sub(r"{\\raise0\.7ex\\hbox{\$ ([a-zA-Z0-9]+) \$}\\!\\mathord{\\left/ {\\vphantom {([a-zA-Z0-9]+) ([a-zA-Z0-9]+)}} \\right\. \\kern-\\nulldelimiterspace}\\!\\lower0\.7ex\\hbox{\$ ([a-zA-Z0-9]+) \$}}", r"\\dfrac{\1}{\4}", changeBoxedTwo)
    fixKernNulldelimiter2 = re.sub(r"{([a-zA-Z]+)\\mathord{\\left/ {\\vphantom {([a-zA-Z]+) ([a-zA-Z]+)\^{([0-9]+)} }} \\right\. \\kern-\\nulldelimiterspace} ([a-zA-Z]+)\^{([0-9]+)} }", r"\\text{\1/\5}^{\6}", fixKernNulldelimiter1)
    fixRm = re.sub(r"{\\rm (\\; )*}", r"\\ ", fixKernNulldelimiter2)
    fixTextbfExtraSpaceB4 = re.sub(r"\\textbf{([ ]*)([^}]+)}", r"\1\\textbf{\2}", fixRm)
    arrayCasesTransform = re.sub(r"\\left\\{\\begin{array}{[a-z]*} ([\s\S]*) \\end{array}\\right\.", r"\\begin{cases} \1 \\end{cases}", fixTextbfExtraSpaceB4)
    fixIncludeGraphics = re.sub(r"\\includegraphics\*\[[^\]]*\]\{", r"\\includegraphics{images/", arrayCasesTransform)
    fixSuperscript = re.sub(r"{[ ]*}\^", r"^", fixIncludeGraphics)
    fixBoldsymbol = re.sub(r"\\boldsymbol{([^}]*)}", r"\1", fixSuperscript)
    fixMathSpacesFinal = fixBoldsymbol.replace('\\ $', '$ ')
    fixDegreeSpaces = re.sub(r"\^\\circ[ ]*\$", r"^\\circ$", fixMathSpacesFinal)
    fixCelsiusError1 = re.sub(r"\^\\circ[ ]*([A-Z]{1})[ ]*\$", r"^\\circ\\text{\1}$", fixDegreeSpaces)
    fixCelsiusError2 = re.sub(r"\^\\circ[ ]*\$([A-Z]{1})([ ]{1})", r"^\\circ\\text{\1}$\2", fixDegreeSpaces)
    fixMoney = re.sub(r"\$R\\\$\\ ([^$]*)\$", r"R\$ \1", fixCelsiusError2)
    final = preamble + '\n' + fixMoney
    
    for line in final:
        depois.write(line)

success = 'Arquivo corrigido COM SUCESSO.'
print(len(success) * '=')
print(success)
print(len(success) * '=')