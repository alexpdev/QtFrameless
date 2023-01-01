from QtFrameless.qt_api import Qt

class Cursor:

    cs = Qt.CursorShape
    m = 6
    loc = {
        0: {
            "id": "topleft",
            "shape": cs.SizeFDiagCursor,
            "range": lambda p, _: p.x() < curs.m and p.y() < curs.m
        },
        1: {
            "id": "topright",
            "shape": cs.SizeBDiagCursor,
            "range": lambda p, r: p.x() >= r.width() - curs.m and p.y() < curs.m
        },
        2: {
            "id": "bottomleft",
            "shape": cs.SizeBDiagCursor,
            "range": lambda p,r: p.y() >= r.height() - curs.m and p.x() < curs.m
        },
        3: {
            "id": "bottomright",
            "shape": cs.SizeFDiagCursor,
            "range": lambda p, r: p.y() >= r.height() - curs.m and p.x() >= r.width() - curs.m
        },
        4: {
            "id": "top",
            "shape": cs.SizeVerCursor,
            "range": lambda p, _: p.y() < curs.m
        },
        5: {
            "id": "bottom",
            "shape": cs.SizeVerCursor,
            "range": lambda p, r: p.y() >= r.height() - curs.m
        },
        6: {
            "id": "left",
            "shape": cs.SizeHorCursor,
            "range": lambda p, _: p.x() < curs.m
        },
        7: {
            "id": "right",
            "shape": cs.SizeHorCursor,
            "range": lambda p, r: p.x() >= r.width() - curs.m
        },
        8: {
            "id": "standard",
            "shape": cs.ArrowCursor,
            "range": lambda _, r: True
        }
    }

    @classmethod
    def match(cls, point, rect, exclusions=None):
        for i in range(len(cls.loc)):
            if exclusions and i not in exclusions:
                matched = cls.loc[i]["range"](point, rect)
                if matched: return cls.loc[i]
        return cls.loc[8]

    @staticmethod
    def resize(old, new, geom, og, direction):
        dx, dy = (new - old).toTuple()
        gx, gy = geom.x(), geom.y()
        gw, gh = geom.width(), geom.height()
        ogw, ogh = og.width(), og.height()
        if direction["id"] == "top":
            return gx, gy + dy, gw, gh - dy
        elif direction["id"] == "left":
            return gx + dx, gy, gw - dx, gh
        elif direction["id"] == "right":
            return gx, gy, ogw + dx, gh
        elif direction["id"] == "bottom":
            return gx, gy, ogw, ogh + dy
        elif direction["id"] == "standard":
            return gx+dx, gy+dy, gw, gh
        elif direction["id"] == "topleft":
            return gx + dx, gy+dy, gw-dx, gh-dy
        elif direction["id"] == "topright":
            return gx, gy+dy, ogw+dx, gh-dy
        elif direction["id"] == "bottomleft":
            return gx + dx, gy, gw - dx, ogh + dy
        elif direction["id"] == "bottomright":
            return gx, gy, ogw + dx, ogh+dy

curs = Cursor
