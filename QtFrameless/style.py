
stylesheet = """
QWidget {
    margin: 2px;
    background-color: #eee;
    color: #000;
    padding: 2px;
}
QMainWindow {
    border: 1px solid ridge;
    background-color: #333;
    color: #000;
    margin: 1px;
    padding: 1px;
}
*[close="true"] {
    border: 1px outset #333;
    border-radius: 9px;
    background-color: #b41605;
}
*[min="true"] {
    border: 1px outset #333;
    border-radius: 9px;
    background-color: #c9c405;
}
*[max="true"] {
    border: 1px outset #333;
    border-radius: 9px;
    background-color: green;
}
*[close="true"]:hover {
    border: 1px outset #333;
    border-radius: 9px;
    background-color: #eb0505;
}
*[min="true"]:hover {
    border: 1px outset #333;
    border-radius: 9px;
    background-color: #f8eb52;
}
*[max="true"]:hover {
    border: 1px outset #333;
    border-radius: 9px;
    background-color: #06e901;
}
*[close="true"]:pressed {
    border: 1px inset #333;
    border-radius: 9px;
    background-color: #c10909;
}
*[min="true"]:pressed {
    border: 1px inset #333;
    border-radius: 9px;
    background-color: #f5e623;
}
*[max="true"]:pressed {
    border: 1px inset #333;
    border-radius: 9px;
    background-color: #22fe1d;
}
"""
