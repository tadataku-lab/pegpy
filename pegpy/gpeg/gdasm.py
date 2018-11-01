import pegpy.gpeg.gparsefunc as gparsefunc
from pegpy.parser import *
from pegpy.peg import *


def gdasm(p, conv=None):
    gsetting('gdasm')
    return generate_gparser(ggenerate(p, 'gdasm'), conv)

def gsetting(f: str):
    if not hasattr(Char, f):
        def emit(pe): return getattr(pe, f)()

        setattr(Empty, f, lambda self: p_True)
        setattr(Any, f, lambda self: gparsefunc.mresult(p_Any))
        setattr(Char, f, gparsefunc.emit_GByte)
        setattr(Range, f, gparsefunc.emit_GByteRange)

        setattr(Seq, f, lambda pe: gparsefunc.emit_GSeq(pe, emit, ParseTree, TreeLink))
        setattr(Ore, f, lambda pe: gparsefunc.emit_GOr(pe, emit))
        setattr(Alt, f, lambda pe: gparsefunc.emit_GAlt(pe, emit, ParseTree, TreeLink))
        setattr(Not, f, lambda pe: gparsefunc.emit_GNot(pe, emit))
        setattr(And, f, lambda pe: gparsefunc.emit_GAnd(pe, emit))
        setattr(Many, f, lambda pe: gparsefunc.emit_GMany(pe, emit, ParseTree, TreeLink))
        setattr(Many1, f, lambda pe: gparsefunc.emit_GMany1(pe, emit, ParseTree, TreeLink))

        setattr(TreeAs, f, lambda pe: gparsefunc.emit_GTreeAs(pe, emit, ParseTree))
        setattr(LinkAs, f, lambda pe: gparsefunc.emit_GLinkAs(pe, emit, TreeLink))
        setattr(FoldAs, f, lambda pe: gparsefunc.emit_GFoldAs(pe, emit, ParseTree, TreeLink))
        setattr(Detree, f, lambda pe: gparsefunc.emit_GDetree(pe, emit))

        # Ref
        memo = {}
        setattr(Ref, f, lambda pe: gparsefunc.emit_Ref(pe, memo, emit))
        return True
    return False

def ggenerate(p, f='gdasm'):
    if not isinstance(p, ParsingExpression):  # Grammar
        p = Ref(p.start().name, p)
    return getattr(p, f)()


class GParserContext:
  __slots__ = ['inputs', 'length', 'pos', 'headpos', 'ast', 'result']

  def __init__(self, inputs, urn='(unknown)', pos=0):
    s = bytes(inputs, 'utf-8') if isinstance(inputs, str) else bytes(inputs)
    self.inputs, self.pos = u.encode_source(s, urn, pos)
    self.length = len(self.inputs)
    self.headpos = self.pos
    self.ast = None
    self.result = {}

def collect_amb(s, pos, result):
    is_first = True
    for result_pos, r in result.items():
        if r == None:
            r = ParseTree("", s, pos, result_pos, None)
        if is_first:
            prev = TreeLink("", r, None)
            is_first = False
        else:
            prev = TreeLink("", r, prev)
    return prev

def generate_gparser(f, conv=None):
    def parse(s, urn='(unknown)', pos=0):
        px = GParserContext(s, urn, pos)
        pos = px.pos
        if not f(px):
            return ParseTree("err", px.inputs, px.headpos, len(s), None)
        elif len(px.result) == 0:
            return ParseTree("", px.inputs, pos, px.pos, None)
        elif len(px.result) == 1:
            (result_pos, result_ast) = list(px.result.items())[0]
            if result_ast == None:
                return ParseTree("", px.inputs, pos, result_pos, None)
            else:
                return result_ast
        return ParseTree("Ambiguity", px.inputs, pos, px.pos, collect_amb(px.inputs, pos, px.result))
    return parse
