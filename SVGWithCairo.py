import cairo
import math
from SVGReader import readSVG
from SVGReader import Transform
import time


class Inscriber:
    def __init__(self, svgcontents = None):
        if (svgcontents == None):
            self.header, self.body = readSVG("askscience.svg")
        else:
            self.header, self.body = svgcontents
        self.w = self.header.viewbox.relwidth
        self.h = self.header.viewbox.relheight

        self.transparentBackground = True

        self.surface_path = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.w, self.h)
        self.ctx_path = cairo.Context(self.surface_path)
        self.ctx_path.scale(self.w, self.h)

        self.surface_circle = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.w, self.h)
        self.ctx_circle = cairo.Context(self.surface_circle)
        self.ctx_circle.scale(self.w, self.h)

        self.surface_text = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.w, self.h)
        self.ctx_text = cairo.Context(self.surface_text)
        self.ctx_text.scale(self.w, self.h)

    def drawPath(self, element):
        if element.isBezier == True:
            self.ctx_path.set_line_width(element.stroke_width / float(self.w) * 2)
            r, g, b = Transform.RGBFromHex(element.stroke)
            self.ctx_path.set_source_rgb(r, g, b)
            x, y = Transform.RelativeFromViewboxCoords(self.header, element.move_to)
            self.ctx_path.move_to(x, y)
            xy1, xy2, xy3 = element.Bezier
            x1, y1 = Transform.RelativeFromViewboxCoords(self.header, xy1)
            x2, y2 = Transform.RelativeFromViewboxCoords(self.header, xy2)
            x3, y3 = Transform.RelativeFromViewboxCoords(self.header, xy3)
            self.ctx_path.curve_to(x1, y1, x2, y2, x3, y3)
            self.ctx_path.stroke()
        else:
            self.ctx_path.set_line_width(element.stroke_width / float(self.w) * 2)
            r, g, b = Transform.RGBFromHex(element.stroke)
            self.ctx_path.set_source_rgb(r, g, b)
            x, y = Transform.RelativeFromViewboxCoords(self.header, element.move_to)
            self.ctx_path.move_to(x, y)    
            x, y = Transform.RelativeFromViewboxCoords(self.header, element.line_to)
            self.ctx_path.line_to(x, y)
            self.ctx_path.stroke()

    def drawCircle(self, element):
        self.ctx_circle.set_line_width(element.stroke_width / float(self.w) * 2)
        r, g, b = Transform.RGBFromHex(element.stroke)
        self.ctx_circle.set_source_rgb(0,0,0)
        x, y = Transform.RelativeFromViewboxCoords(self.header, element.xy)
        self.ctx_circle.arc(x, y, element.r / float(self.w) * 2, 0, 2 * math.pi)
        self.ctx_circle.stroke_preserve()
        
        r, g, b = Transform.RGBFromHex(element.fill)
        self.ctx_circle.set_source_rgb(r, g, b)
        self.ctx_circle.fill()

    def drawArrow(self, element):
        r, g, b = Transform.RGBFromHex(element.fill)
        self.ctx_path.set_source_rgb(r, g, b)
        start = True
        for p in element.points:
            x, y = Transform.RelativeFromViewboxCoords(self.header, p)
            if start == True:
                self.ctx_path.move_to(x, y)
                start = False
            else:
                self.ctx_path.line_to(x, y)
        self.ctx_path.close_path()
        self.ctx_path.fill()

    def drawText(self, element):
        r, g, b = Transform.RGBFromHex(element.fill)
        self.ctx_text.set_source_rgb(r, g, b)
        self.ctx_text.select_font_face(element.fontFamily)
        self.ctx_text.set_font_size(element.fontsize / float(self.w))
        x, y = Transform.RelativeFromViewboxCoords(self.header, element.xy)
        self.ctx_text.move_to(x, y)
        self.ctx_text.show_text(element.text)
        self.ctx_text.stroke()

    def renderSVG(self, ctx):
        if not self.transparentBackground:
            ctx.set_source_rgb(255,255,255)
            ctx.rectangle(0, 0, 1, 1)
            ctx.stroke()

        startdrawing = time.time()
        for e in self.body:
            if e.type == "path":
                self.drawPath(e)
            elif e.type == "circle":
                self.drawCircle(e)
            elif e.type == "polyline":
                self.drawArrow(e)
            elif e.type == "text":
                self.drawText(e)
        enddrawing = time.time()
        self.rendertime = enddrawing - startdrawing

        ctx.identity_matrix()
        ctx.set_source_surface(self.surface_path, 0, 0)
        ctx.paint()
        ctx.set_source_surface(self.surface_circle, 0, 0)
        ctx.paint()
        ctx.set_source_surface(self.surface_text, 0, 0)
        ctx.paint()

if __name__ == '__main__':
    header, body = readSVG("askscience.svg")
    w = header.viewbox.relwidth
    h = header.viewbox.relheight
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surface)
    ctx.scale(w, h)
    inscriber = Inscriber((header, body))
    inscriber.transparentBackground = False
    inscriber.renderSVG(ctx)
    print "Writing to file."


    startwrite = time.time()
    surface.write_to_png("askscience.png")
    endwrite = time.time()
    print "File written. Time elapsed: %.2fs" % (endwrite - startwrite)
