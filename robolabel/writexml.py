import xml.dom.minidom as Dom
from xml.dom import minidom

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
lb = Blueprint('writexml', __name__, url_prefix='/xml')

def writexml(annotations,filename,width,height):
    doc = Dom.Document()
    root_node = doc.createElement("annotation")
    doc.appendChild(root_node)
    f_node = doc.createElement("folder")
    f_value = doc.createTextNode("cam")
    f_node.appendChild(f_value)
    root_node.appendChild(f_node)

    ff_node = doc.createElement("filename")
    ff_value = doc.createTextNode(filename)
    ff_node.appendChild(ff_value)
    root_node.appendChild(ff_node)

    r_node = doc.createElement("relpath")
    r_value = doc.createTextNode("../cam/"+filename)
    r_node.appendChild(r_value)
    root_node.appendChild(r_node)

    head = doc.createElement("source")

    d_node = doc.createElement("database")
    d_value = doc.createTextNode("Unknown")
    d_node.appendChild(d_value)
    head.appendChild(d_node)
    root_node.appendChild(head)

    size= doc.createElement("size")
    w_node = doc.createElement("width")
    w_value = doc.createTextNode(str(width))
    w_node.appendChild(w_value)
    h_node = doc.createElement("height")
    h_value = doc.createTextNode(str(height))
    h_node.appendChild(h_value)
    dp_node = doc.createElement("depth")
    dp_value = doc.createTextNode("1")
    dp_node.appendChild(dp_value)
    size.appendChild(w_node)
    size.appendChild(h_node)
    size.appendChild(dp_node)
    root_node.appendChild(size)


    
    sg_node = doc.createElement("segmented")
    sg_value = doc.createTextNode("0")
    sg_node.appendChild(sg_value)
    root_node.appendChild(sg_node)
    for ann in annotations:
        ob_node= doc.createElement("object")
        name_node = doc.createElement("name")
        name_value = doc.createTextNode(ann["tag"])
        name_node.appendChild(name_value)
        pose_node = doc.createElement("pose")
        pose_value = doc.createTextNode("Unspecified")
        pose_node.appendChild(pose_value)
        tru_node = doc.createElement("truncated")
        tru_value = doc.createTextNode("0")
        tru_node.appendChild(tru_value)
        diff_node= doc.createElement("difficult")
        diff_value= doc.createTextNode("0")
        diff_node.appendChild(diff_value)
        bnd_node=doc.createElement("bndbox")

        xmin_node = doc.createElement("xmin")
        xmin_value = doc.createTextNode(str(round(ann["x"])))
        xmin_node.appendChild(xmin_value)

        ymin_node = doc.createElement("ymin")
        ymin_value = doc.createTextNode(str(round(ann["y"])))
        ymin_node.appendChild(ymin_value)

        xmax_node = doc.createElement("xmax")
        xmax_value = doc.createTextNode(str(round(ann["x"]+ann["width"])))
        xmax_node.appendChild(xmax_value)

        ymax_node = doc.createElement("ymax")
        ymax_value = doc.createTextNode(str(round(ann["y"]+ann["height"])))
        ymax_node.appendChild(ymax_value)

        bnd_node.appendChild(xmin_node)
        bnd_node.appendChild(ymin_node)
        bnd_node.appendChild(xmax_node)
        bnd_node.appendChild(ymax_node)

        ob_node.appendChild(name_node)
        ob_node.appendChild(pose_node)
        ob_node.appendChild(tru_node)
        ob_node.appendChild(diff_node)
        ob_node.appendChild(bnd_node)
        root_node.appendChild(ob_node)



    print (doc.toxml("utf-8"))
    terms=filename.split(".")
    f = open(terms[0]+".xml", "wb")
    f.write(doc.toprettyxml(indent="\t", newl="\n", encoding="utf-8"))
    f.close()