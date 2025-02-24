#!/usr/bin/env python3

k = 4

def document(contents = r"\draw [red] (0,0) rectangle (1,1);"):
    ret = r"""\documentclass{standalone}
\usepackage{tikz}
\usetikzlibrary{matrix,positioning,fit,arrows.meta}
\begin{document}
\begin{tikzpicture}
"""
    ret += contents
    ret += r"""
\end{tikzpicture}
\end{document}
"""
    return ret

def km_string(km, nodes=False):
    if nodes:
        return " & ".join(f"\\node {{{'\\$' if v == '$' else v}}};" for v in km)
    return " & ".join("\\$" if v == "$" else v for v in km)

def sbwt(kmers = None, loc = "", name = "sbwt", new=set()):
    if kmers is None:
        kmers = [
            ("$$$$", False, True, False, False),
            ("$$$C", False, True, False, False),
            ("$$CC", False, True, False, False),
            ("$CCC", False, True, False, False),
            ("CCCC", False, False, False, False)
        ]
    ret = f"\\matrix ({name})" 
    ret += f"[{loc}," if len(loc) > 0 else "["
    ret += "nodes={minimum height=1.5em},style={gray,column sep={0.7em,between origins},row sep=-\\pgflinewidth},\n"
    k = len(kmers[0][0])
    ret += f"column {k}/.style={{column sep={{1.5em,between origins}}}},"
    ret += ",".join(f"\ncolumn {i}/.style={{black,column sep={{1.5em,between origins}},nodes={{draw,minimum width=1.5em}}}}" for i in range(k + 1, k + 5))
    ret += "] {\n"
    for km in kmers:
        ret += km_string(km[0], True) + " & "
        ret += " & ".join(f"\\node{'[fill=green!20]' if km[0] in new else ''} {{{'1' if v else '0'}}};" for v in km[1:])
        ret += "\\\\\n"
    ret += "};\n"
    return ret

def strings(string_list = None, loc = "", name = "strings"):
    if string_list is None:
        string_list = [
            "ACGTACT",
            "CATTATTAC"
        ]
    ret = f"\\matrix ({name})" 
    if len(loc) > 0:
        ret += f" [{loc}]"
    ret += " {\n"
    for s in string_list:
        ret += f"\\node[right] {{{s}}};\\\\\n"
    ret += "};\n"
    return ret

def title(label, ref):
    return f"\\node[above=0.1em of {ref}] ({ref + '-lab'}) {{{label}}};\n"

def xor_table(table = None, loc = "", name = "xorT"):
    if table is None:
        table = [
            (False, True, False, False),
            (False, True, False, False),
            (False, True, False, False),
            (False, True, False, False),
            (False, False, False, False)
        ]
    ret = f"\\matrix ({name})"
    ret += f"[{loc}," if len(loc) > 0 else "["
    ret += "nodes={minimum height=1.5em},style={column sep={1.5em,between origins},row sep=-\\pgflinewidth},nodes={draw,minimum width=1.5em}] {\n"
    for line in table:
        ret += " & ".join("\\node[text=red] {1};" if v else "\\node {0};" for v in line) + "\\\\\n"
    ret += "};"
    return ret

def buffer(kmers = None, edges = False, loc = "", name = "buffer", highlight=None):
    if kmers is None:
        kmers = [
            ("AAAA", False, True, False, False),
            ("AAAC", False, True, False, False),
            ("AACC", False, True, False, False),
            ("ACCC", False, True, False, False),
            ("CCCC", False, False, False, False)
        ]
    ret = f"\\matrix ({name})" 
    ret += f"[{loc}," if len(loc) > 0 else "["
    ret += f"nodes={{minimum height=1.5em}},style={{matrix of nodes,column sep={{0.7em,between origins}},row sep=-\\pgflinewidth}},\n"
    k = len(kmers[0][0])
    ret += f"column {k}/.style={{column sep={{1.5em,between origins}}}},"
    ret += ",".join(f"\ncolumn {i}/.style={{column sep={{1.5em,between origins}},nodes={{draw,minimum width=1.5em}}}}" for i in range(k + 1, k + 5))
    ret += "] {\n"
    for km in kmers:
        ret += km_string(km[0]) + " & "
        if edges:
            ret += " & ".join("1" if v else "0" for v in km[1:])
        ret += "\\\\\n"
    ret += "};\n"
    if not highlight is None:
        ret += f"\\begin{{scope}}[blend mode=overlay,overlay]\n  \\fill[fill={highlight}] ({name}.north west) rectangle ({name}.south east);\n\\end{{scope}}\n"
    return ret

def rem(initial_kmers, xort_t, removables, loc = "", name = "rem"):
    ret = f"\\matrix ({name})"
    ret += f"[{loc}," if len(loc) > 0 else "["
    ret += "nodes={draw,minimum width=1.5em,minimum height=1.5em},style={column sep={1.5em,between origins},row sep=-\\pgflinewidth}] {\n"
    for km, xor_line in zip(initial_kmers, xort_t):
        fill = "fill=red!20" if km[0] in removables else ""
        ret += " & ".join(
            f"\\node[{fill + ',' if len(fill) > 0 else ''}text=red] {{{'1' if v ^ x else '0'}}};" if x 
            else f"\\node{'[' + fill + "]" if len(fill) > 0 else ''} {{{'1' if v else '0'}}};"
            for v, x in zip(km[1:], xor_line)
        )
        ret += "\\\\\n"
    ret += "};\n"
    return ret

def arrow(f_lab, t_lab, angles=None, tt_lab=None, t_ang=None, ttt_lab=None, tt_ang=None):
    ret = "\\begin{scope}[transparency group, opacity=0.3]\n"
    ret += f"  \\draw[-latex,line width=3pt] ({f_lab}) {'--' if angles is None else angles} ({t_lab})"
    if not tt_lab is None:
        ret += f" {'--' if t_ang is None else t_ang} ({tt_lab})"
    if not ttt_lab is None:
        ret += f" {'--' if tt_ang is None else tt_ang} ({ttt_lab})"
    ret += ";\n\\end{scope}"
    return ret

def add_pic():
    init_sbwt = [
        ("$$$$$$", 0, 1, 0, 0),
        ("$$$$CA", 0, 0, 0, 1),
        ("GGTATA", 0, 0, 0, 1),
        ("ACGGTA", 0, 0, 0, 1),
        ("$CATTA", 0, 0, 0, 1),
        ("TTATTA", 0, 1, 0, 0),
        ("$$$$$C", 1, 0, 0, 0),
        ("TATTAC", 0, 0, 1, 0),
        ("ATTACG", 0, 0, 1, 0),
        ("TTACGG", 0, 0, 0, 1),
        ("$$$CAT", 0, 0, 0, 1),
        ("GTATAT", 0, 0, 0, 0),
        ("CGGTAT", 1, 0, 0, 0),
        ("CATTAT", 0, 0, 0, 1),
        ("TACGGT", 1, 0, 0, 0),
        ("$$CATT", 1, 0, 0, 0),
        ("ATTATT", 1, 0, 0, 0)
    ]
    buf_precalc = [
        ("CATTAA", 0, 0, 0, 1),
        ("TTAATA", 0, 1, 0, 0),
        ("CCATTA", 1, 0, 0, 0),
        ("TAATAC", 0, 0, 1, 0),
        ("AATACG", 0, 0, 1, 0),
        ("ATACGG", 0, 0, 0, 0),
        ("ATTAAT", 1, 0, 0, 0)
    ]

    buf_elems = [
        ("CATTAA", 0, 0, 0, 1),
        ("TTAATA", 0, 1, 0, 0),
        ("CCATTA", 1, 0, 0, 1),
        ("TAATAC", 0, 0, 1, 0),
        ("AATACG", 0, 0, 1, 0),
        ("ATACGG", 0, 0, 0, 1),
        ("ATTAAT", 1, 0, 0, 0)
    ]
    xor_tab = [
        (0, 0, 0, 0), 
        (0, 0, 0, 1), 
        (0, 0, 0, 0), 
        (0, 0, 0, 0), 
        (0, 0, 0, 0), 
        (0, 0, 0, 0), 
        (1, 1, 0, 0), 
        (0, 0, 0, 0), 
        (0, 0, 0, 0), 
        (0, 0, 0, 1), 
        (0, 0, 0, 1), 
        (0, 0, 0, 0), 
        (0, 0, 0, 0), 
        (0, 0, 0, 0), 
        (0, 0, 0, 0), 
        (1, 0, 0, 0), 
        (0, 0, 0, 0)
    ]

    rem_dum = [
        init_sbwt[i] for i in (1, 4, 10, 15)
    ]
    add_dum = [
        ("$$$CCA", 0, 0, 0, 1),
        ("$$$$CC", 1, 0, 0, 0),
        ("$$CCAT", 0, 0, 0, 1),
        ("$CCATT", 1, 0, 0, 0)
    ]

    final_sbw = [
        ("$$$$$$", 0, 1, 0, 0),
        ("CATTAA", 0, 0, 0, 1),
        ("$$$CCA", 0, 0, 0, 1),
        ("TTAATA", 0, 1, 0, 0),
        ("GGTATA", 0, 0, 0, 1),
        ("ACGGTA", 0, 0, 0, 1),
        ("CCATTA", 1, 0, 0, 1),
        ("TTATTA", 0, 1, 0, 0),
        ("$$$$$C", 0, 1, 0, 0),
        ("TAATAC", 0, 0, 1, 0),
        ("TATTAC", 0, 0, 1, 0),
        ("$$$$CC", 1, 0, 0, 0),
        ("AATACG", 0, 0, 1, 0),
        ("ATTACG", 0, 0, 1, 0),
        ("ATACGG", 0, 0, 0, 1),
        ("TTACGG", 0, 0, 0, 0),
        ("ATTAAT", 1, 0, 0, 0),
        ("$$CCAT", 0, 0, 0, 1),
        ("GTATAT", 0, 0, 0, 0),
        ("CGGTAT", 1, 0, 0, 0),
        ("CATTAT", 0, 0, 0, 1),
        ("TACGGT", 1, 0, 0, 0),
        ("$CCATT", 1, 0, 0, 0),
        ("ATTATT", 1, 0, 0, 0)
    ]
    add_set = {
        d[0] for d in add_dum
    }.union({
        e[0] for e in buf_elems
    })
    ins_strings = ["CCATTAATACGGTAT"]
    k = 6

    print(document(
        sbwt(init_sbwt, "", "initial") + title("initial SBWT", "initial") + 
        buffer(buf_elems, False, "above=of initial-lab", "inskm", "green!20") + title("filtered k-mers", "inskm") +
        strings(ins_strings, "above=of inskm-lab", "insert") + title("addable seq", "insert") +
        xor_table(xor_tab, "right=of initial", "xorT") + title("xor table", "xorT") + 
        buffer(buf_elems, True, "right=of inskm", "belem", "green!20") + title("buffer with final edges", "belem") + 
        buffer(buf_precalc, True, "above=of belem", "prec", "green!20") + title("buffer with internal edges", "prec") + 
        buffer(rem_dum, False, "right=of belem-lab.south east", "remdum", "red!20") + title("removable dummies", "remdum") + 
        buffer(add_dum, True, "right=of remdum", "addum", "green!20") + title("addable dummies", "addum") + 
        rem(init_sbwt, xor_tab, {e[0] for e in rem_dum}, "right=of xorT", "remmed") + title("xor and dummy removal", "remmed") + 
        sbwt(final_sbw, "right=of remmed", "final", add_set) + title("final merged SBWT", "final") + "\n" +
        arrow("initial-lab.north", "inskm.south") +
        arrow("initial.east", "xorT.west") +
        arrow("xorT.east", "remmed.west") +
        arrow("remmed.east", "final.west") +
        arrow("insert.south", "[yshift=-5pt]inskm-lab.north") +
        arrow("inskm.north east", "prec.south west", "to [out=45,in=-135]") +
        arrow("prec.south", "[yshift=-5pt]belem-lab.north") +
        arrow("[yshift=2em]prec.east", "[yshift=-5pt]remdum-lab.north", "to [out=0,in=90]") +
        arrow("[yshift=2em]prec.east", "[yshift=-5pt]addum-lab.north", "to [out=0,in=90]") +
        arrow("belem.east", "[xshift=5em]belem.east", "to [out=0,in=180]", "[yshift=-5pt]final-lab.north west", "to [out=0,in=135]") + 
        arrow("[xshift=-1em]initial.north east", "[yshift=1em]xorT-lab.north west", "to [out=90,in=180]", "[xshift=2em]belem.south", "to [out=0,in=-90]") + 
        arrow("[xshift=-1em]initial.north east", "[yshift=1em]xorT-lab.north west", "to [out=90,in=180]", "[yshift=1em,xshift=4em]xorT-lab.north west", "to [out=0,in=180]", "[xshift=-1.5em]remdum.south", "to [out=0,in=-90]") + 
        arrow("[xshift=-1em]initial.north east", "[yshift=1em]xorT-lab.north west", "to [out=90,in=180]", "[yshift=1em,xshift=4em]xorT-lab.north west", "to [out=0,in=180]", "[xshift=-4em]addum.south", "to [out=0,in=-135]") + 
        arrow("belem.south", "[yshift=-5pt]belem.south |- xorT-lab.north", "to [out=-90,in=90]") + 
        arrow("remdum.south", "[yshift=-5pt]remmed-lab.north", "to [out=-90,in=90]") + 
        arrow("addum.south", "[yshift=-5pt]final-lab.north", "to [out=-90,in=90]") + 
        arrow("initial.south east", "remmed.south west", "to [out=-30,in=-150]") + "\n"
    ))

def rem_pic():
    initial_sbwt = [
        ("$$$$$$", 1, 1, 0, 0),
        ("$$$$$A", 1, 0, 0, 0),
        ("$$$$AA", 0, 0, 0, 1),
        ("ATCCAA", 0, 0, 0, 0),
        ("$$$$CA", 0, 0, 0, 1),
        ("CATCCA", 1, 0, 0, 0),
        ("GATTCA", 0, 0, 0, 1),
        ("ATTAGA", 0, 0, 0, 1),
        ("$AATTA", 0, 0, 1, 0),
        ("$CATTA", 0, 0, 1, 0),
        ("$$$$$C", 1, 0, 0, 0),
        ("TCATCC", 1, 0, 0, 0),
        ("TTCATC", 0, 1, 0, 0),
        ("AGATTC", 1, 0, 0, 0),
        ("AATTAG", 1, 0, 0, 0),
        ("CATTAG", 0, 0, 0, 0),
        ("$$$AAT", 0, 0, 0, 1),
        ("$$$CAT", 0, 0, 0, 1),
        ("ATTCAT", 0, 1, 0, 0),
        ("TTAGAT", 0, 0, 0, 1),
        ("$$AATT", 1, 0, 0, 0),
        ("$$CATT", 1, 0, 0, 0),
        ("TAGATT", 0, 1, 0, 0)
    ]
    belems = [
        ("ATTAGA", 0, 0, 0, 1),
        ("AATTAG", 1, 0, 0, 0),
        ("TTAGAT", 0, 0, 0, 1),
        ("TAGATT", 0, 0, 0, 0)
    ]
    removable_dummies = [
        initial_sbwt[i] for i in (2, 8, 16, 20)
    ]
    addable_dummies = [
        ("$$$AGA", 0, 0, 0, 1),
        ("$$$$AG", 1, 0, 0, 0),
        ("$$AGAT", 0, 0, 0, 1),
        ("$AGATT", 0, 1, 0, 0)
    ]
    xor_tab = [
        (0, 0, 0, 0),
        (1, 0, 1, 0),
        (0, 0, 0, 1),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (1, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0)
    ]
    xorred = [
        (1, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 1),
        (1, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 0, 1),
        (0, 0, 0, 0),
        (0, 0, 1, 0),
        (1, 0, 0, 0),
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (1, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 0),
        (0, 0, 0, 1),
        (0, 1, 0, 0),
        (0, 0, 0, 1),
        (0, 0, 0, 0),
        (1, 0, 0, 0),
        (0, 1, 0, 0)
    ]
    final_sbwt = [
        ("$$$$$$", 1, 1, 0, 0),
        ("$$$$$A", 0, 0, 1, 0),
        ("ATCCAA", 0, 0, 0, 0),
        ("$$$$CA", 0, 0, 0, 1),
        ("CATCCA", 1, 0, 0, 0),
        ("GATTCA", 0, 0, 0, 1),
        ("$$$AGA", 0, 0, 0, 1),
        ("$CATTA", 0, 0, 1, 0),
        ("$$$$$C", 1, 0, 0, 0),
        ("TCATCC", 1, 0, 0, 0),
        ("TTCATC", 0, 1, 0, 0),
        ("AGATTC", 1, 0, 0, 0),
        ("$$$$AG", 1, 0, 0, 0),
        ("CATTAG", 0, 0, 0, 0),
        ("$$$CAT", 0, 0, 0, 1),
        ("ATTCAT", 0, 1, 0, 0),
        ("$$AGAT", 0, 0, 0, 1),
        ("$$CATT", 1, 0, 0, 0),
        ("$AGATT", 0, 1, 0, 0)
    ]
    rem_strings = ["AATTAGATT"]
    k = 6

    rem_set = {
        d[0] for d in removable_dummies
    }.union({
        e[0] for e in belems
    })

    print(document(
        sbwt(initial_sbwt, "", "initial") + title("initial SBWT", "initial") + 
        buffer(belems, False, "above=of initial-lab", "remkm", "red!20") + title("filtered k-mers", "remkm") +
        strings(rem_strings, "above=of remkm-lab", "rem") + title("removable seq", "rem") +
        xor_table(xor_tab, "right=of initial", "xorT") + title("xor table", "xorT") + 
        buffer(belems, True, "right=of remkm.north east", "belem", "red!20") + title("buffer with internal edges", "belem") + 
        buffer(removable_dummies, False, "right=of belem.east", "remdum", "red!20") + title("removable dummies", "remdum") + 
        buffer(addable_dummies, True, "right=of remdum", "addum", "green!20") + title("addable dummies", "addum") + 
        rem(initial_sbwt, xor_tab, rem_set, "right=of xorT", "remmed") + title("xor and dummy removal", "remmed") + 
        sbwt(final_sbwt, "right=of remmed", "final", {b[0] for b in addable_dummies}) + title("final merged SBWT", "final") + "\n" +
        arrow("initial-lab.north", "remkm.south") +
        arrow("initial.east", "xorT.west") +
        arrow("xorT.east", "remmed.west") +
        arrow("remmed.east", "final.west") + 
        arrow("rem", "[yshift=-5pt]remkm-lab.north") + 
        arrow("[yshift=1em]remkm.south east", "[xshift=1em]belem.south west", "to [out=0,in=-135]") + 
        arrow("belem.east", "remdum.west") + 
        arrow("belem.north east", "addum.north west", "to [out=45,in=135]") + 
        arrow("belem.south", "[yshift=-5pt]xorT-lab.north", "to [out=-90,in=90]") + 
        arrow("[xshift=1em]belem.south", "[yshift=-5pt,xshift=-1em]remmed-lab.north", "to [out=-90,in=90]") + 
        arrow("remdum.south", "[yshift=-5pt]remmed-lab.north", "to [out=-90,in=90]") + 
        arrow("addum.south", "final-lab.north", "to [out=-90,in=90]") + 
        arrow("initial.south east", "remmed.south west", "to [out=-15,in=-165]") +
        arrow("[xshift=-1em]initial.north east", "[yshift=2em]xorT-lab.north west", "to [out=90,in=180]", "[yshift=2em,xshift=4em]xorT-lab.north west", "to [out=0,in=180]", "[xshift=2em]remdum.south west", "to [out=0,in=-120]") + 
        arrow("[xshift=-1em]initial.north east", "[yshift=2em]xorT-lab.north west", "to [out=90,in=180]", "[yshift=2em,xshift=12em]xorT-lab.north west", "to [out=0,in=180]", "[xshift=2em]addum.south west", "to [out=0,in=-120]") + "\n"
    ))


if __name__ == "__main__":
    rem_pic()
    exit()
    add_pic()