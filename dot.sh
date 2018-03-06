python dev.py > /tmp/dot.dot
cat /tmp/dot.dot | dot -Tpng > dot.png
