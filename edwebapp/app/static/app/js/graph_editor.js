const svgElement = document.getElementById("my-svg");

function clearSvg() {
    var circles = svgElement.getElementsByTagName("circle");
    while (circles.length > 0) {
      var circle = circles[0];
      circle.parentNode.removeChild(circle);
    }
    var texts = svgElement.getElementsByTagName("text");
    while (texts.length > 0) {
      var text = texts[0];
      text.parentNode.removeChild(text);
    }
    var lines = svgElement.getElementsByTagName("line");
    while (lines.length > 0) {
      var line = lines[0];
      line.parentNode.removeChild(line);
    }
}
class TreeNode {
    constructor(value, height) {
        this.value = value;
        this.height = height;
        this.left = null;
        this.right = null;
    }
}

class BinarySearchTree {
    constructor() {
        this.root = null;
        this.height = 0;
    }

    insert(value) {
        if (!this.root) {
            this.root = new TreeNode(value, 0);
            this.height = 0;
            return;
        }

        let currentNode = this.root;
        let parentNode = null;
        let height = 0;

        while (currentNode) {
            parentNode = currentNode;

            if (parseFloat(value) < parseFloat(currentNode.value)) {
                currentNode = currentNode.left;
            } else {
                currentNode = currentNode.right;
            }
            height++;

        }
        if (height > 3) {
                alert("дерево надто високе та не вміщається");
                return;
        }

        if (parseFloat(value) < parseFloat(parentNode.value)) {
            console.log(value, parentNode.value);
            parentNode.left = new TreeNode(value, height);
        } else {
            parentNode.right = new TreeNode(value, height);
        }

        this.height = Math.max(this.height, height - 1);
    }

    drawBST(node, elementSvg, pos_x, pos_y, prev_x, prev_y) {
        if (node === null) return;

        var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", pos_x + "%");
        circle.setAttribute("cy", pos_y + "%");
        circle.setAttribute("r", "20");
        circle.setAttribute("fill", "blue");

        var text = document.createElementNS("http://www.w3.org/2000/svg", "text");

        var test_y = pos_y + 1;
        text.setAttribute("x", pos_x + "%");
        text.setAttribute("y", test_y + "%");
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("fill", "white");
        text.textContent = node.value;

        var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        if (prev_x > 0) {

            var distance = Math.sqrt((pos_x - prev_x) ** 2 + (pos_y - prev_y) ** 2);
            var ratio = 4.5 / distance;
            var new_x = prev_x + (pos_x - prev_x) * ratio;
            var new_y = prev_y + (pos_y - prev_y) * ratio;

            line.setAttribute("x1", new_x + "%");
            line.setAttribute("y1", new_y + "%");
            line.setAttribute("x2", pos_x + "%");
            line.setAttribute("y2", pos_y + "%");
            line.setAttribute("stroke", "black");
            line.setAttribute("stroke-width", "2");
            elementSvg.appendChild(line);
        }

        prev_x = pos_x;
        prev_y = pos_y;

        elementSvg.appendChild(circle);
        elementSvg.appendChild(text);
        var pos_x_left = pos_x - (this.height - node.height + 1) / (node.height / 2 + 1) * 7
        var pos_x_right = pos_x + (this.height - node.height + 1)/ (node.height / 2 + 1) * 7
        var pos_y_new = pos_y + 23

        this.drawBST(node.left, elementSvg, pos_x_left, pos_y_new, prev_x, prev_y);
        this.drawBST(node.right, elementSvg, pos_x_right, pos_y_new, prev_x, prev_y);
    }

    clearBST() {
        this.root = null;
        this.height = 0;
    }
}



class Graph {
    constructor() {
        this.vertices = [];
        this.edges = [];
        this.captions = [];
        this.line = [];
    }

    addVertex(x, y, color) {
        const vertex = { x, y, color };
        this.vertices.push(vertex);
    }

    addLinePoints(x, y) {
        const point = { x, y };
        this.line.push(point);
    }

    clearLinePoints() {
        this.line = [];
    }

    addEdge(x1, y1, x2, y2, color) {
        const edge = { x1, y1, x2, y2, color };
        this.edges.push(edge);
    }

    addCaption(x, y, text, color) {
        const caption = { x, y, text, color };
        this.captions.push(caption);
    }

    clearGraph() {
        this.vertices = [];
        this.edges = [];
        this.captions = [];
        this.line = [];
    }

    drawGraph() {
        clearSvg()
        for (var edge of this.edges) {
            var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", edge.x1 + "%");
            line.setAttribute("y1", edge.y1 + "%");
            line.setAttribute("x2", edge.x2 + "%");
            line.setAttribute("y2", edge.y2 + "%");
            line.setAttribute("stroke", edge.color);
            line.setAttribute("stroke-width", "2");
            svgElement.appendChild(line);
        }

        for (let vertex of this.vertices) {
            var circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            circle.setAttribute("cx", vertex.x + "%");
            circle.setAttribute("cy", vertex.y + "%");
            circle.setAttribute("r", "20");
            circle.setAttribute("fill", vertex.color);
            svgElement.appendChild(circle);
        }

        for (let caption of this.captions) {
            var text = document.createElementNS("http://www.w3.org/2000/svg", "text");
            text.setAttribute("x", caption.x + "%");
            text.setAttribute("y", caption.y + "%");
            text.setAttribute("text-anchor", "middle");
            text.setAttribute("fill", caption.color);
            text.textContent = caption.text;
            svgElement.appendChild(text);
        }
        var svgCode = svgElement.outerHTML;
        document.getElementById("hidden-input").value = svgCode;
    }
}

var addEdge = document.getElementById("add-edge");
const bst = new BinarySearchTree();
const graph = new Graph();
var status = 0;
var modeGraph = 1;

addEdge.addEventListener("click", function(event) {

    var edge = document.getElementById("input-edge-bst").value;
    bst.insert(edge)
    clearSvg()
    bst.drawBST(bst.root, svgElement, 50, 15, -1, -1);

    var svgCode = svgElement.outerHTML;
    document.getElementById("hidden-input").value = svgCode;
});



var taskTypeSelect = document.getElementById('taskType');
var svgBlock = document.getElementById("svg-block");
var graphBlock = document.getElementById('graph-block');
var bstBlock = document.getElementById('bst-block');
var btnClear = document.getElementById('clear-img');


btnClear.addEventListener("click", ()=> {
    clearSvg();
    bst.clearBST();
});

taskTypeSelect.addEventListener('change', function() {

    var selectedValue = taskTypeSelect.value;
    switch (selectedValue) {
        case '1':
            svgBlock.classList.add("hidden-element");
            graphBlock.classList.add("hidden-element");
            bstBlock.classList.add("hidden-element");
            btnClear.classList.add("hidden-element");
            status = 0;
            clearSvg()
            graph.clearGraph()
            bst.clearBST()
            break;
        case '2':
            svgBlock.classList.remove("hidden-element");
            graphBlock.classList.remove("hidden-element");
            bstBlock.classList.add("hidden-element");
            btnClear.classList.remove("hidden-element");
            status = 1;
            clearSvg()
            bst.clearBST()
            break;
        case '3':
            svgBlock.classList.remove("hidden-element");
            graphBlock.classList.add("hidden-element");
            bstBlock.classList.remove("hidden-element");
            btnClear.classList.remove("hidden-element");
            status = 0;
            graph.clearGraph()
            clearSvg()
            break;
    }
});

var addVertexBtn = document.getElementById("add-vertex-btn");
var addLineBtn = document.getElementById("add-line-btn");
var addCaptionBtn = document.getElementById("add-caption-btn");
var addVertex = document.getElementById("add-vertex");
var addLine = document.getElementById("add-line");
var addCaption = document.getElementById("add-caption");

addVertexBtn.addEventListener("click", function(event) {
    addVertexBtn.classList.remove("btn-secondary");
    addVertexBtn.classList.add("btn-primary");
    addLineBtn.classList.remove("btn-primary");
    addLineBtn.classList.add("btn-secondary");
    addCaptionBtn.classList.remove("btn-primary");
    addCaptionBtn.classList.add("btn-secondary");

    addVertex.classList.remove("hidden-element");
    addLine.classList.add("hidden-element");
    addCaption.classList.add("hidden-element");
    modeGraph = 1;
    graph.clearLinePoints();
});

addLineBtn.addEventListener("click", function(event) {
    addVertexBtn.classList.remove("btn-primary");
    addVertexBtn.classList.add("btn-secondary");
    addLineBtn.classList.remove("btn-secondary");
    addLineBtn.classList.add("btn-primary");
    addCaptionBtn.classList.remove("btn-primary");
    addCaptionBtn.classList.add("btn-secondary");

    addVertex.classList.add("hidden-element");
    addLine.classList.remove("hidden-element");
    addCaption.classList.add("hidden-element");
    modeGraph = 2;
});

addCaptionBtn.addEventListener("click", function(event) {
    addVertexBtn.classList.remove("btn-primary");
    addVertexBtn.classList.add("btn-secondary");
    addLineBtn.classList.remove("btn-primary");
    addLineBtn.classList.add("btn-secondary");
    addCaptionBtn.classList.remove("btn-secondary");
    addCaptionBtn.classList.add("btn-primary");


    addVertex.classList.add("hidden-element");
    addLine.classList.add("hidden-element");
    addCaption.classList.remove("hidden-element");
    modeGraph = 3;
    graph.clearLinePoints();
});

const colorVertex = document.getElementById('color-vertex');
const colorValue = document.getElementById('color-value');
const vertexValue = document.getElementById('vertex-value');

const captionText = document.getElementById('caption-text');
const captionColor = document.getElementById('caption-color');
const edgeColor = document.getElementById('color-edge');



svgElement.addEventListener("click", function(event) {
    if (status == 1){

        if (modeGraph == 1) {
            const svgWidth = svgElement.clientWidth;
            const svgHeight = svgElement.clientHeight;
            var p_x = event.offsetX / svgWidth * 100;
            var p_y = event.offsetY / svgHeight * 100;
            graph.addVertex(p_x, p_y, colorVertex.value);
            if (vertexValue.value.length > 0) {
                graph.addCaption(p_x, p_y + 1, vertexValue.value, colorValue.value);
            }
            graph.drawGraph();
        }
        if (modeGraph == 2) {
            const svgWidth = svgElement.clientWidth;
            const svgHeight = svgElement.clientHeight;
            var p_x = event.offsetX / svgWidth * 100;
            var p_y = event.offsetY / svgHeight * 100;
            var new_x = -1;
            var new_y = -1;
            for (var vertex of graph.vertices) {
                if (Math.abs(vertex.x - p_x) < 3 && Math.abs(vertex.y - p_y) < 4.5){
                    new_x = vertex.x;
                    new_y = vertex.y;
                }
            }
            if (new_x > 0) {
                graph.addLinePoints(new_x, new_y);
                if (graph.line.length > 1) {
                    graph.addEdge(graph.line[0].x, graph.line[0].y, graph.line[1].x, graph.line[1].y, edgeColor.value);
                    graph.clearLinePoints();
                    graph.drawGraph();
                }
            }
        }
        if (modeGraph == 3) {
            const svgWidth = svgElement.clientWidth;
            const svgHeight = svgElement.clientHeight;
            var p_x = event.offsetX / svgWidth * 100;
            var p_y = event.offsetY / svgHeight * 100;
            graph.addCaption(p_x, p_y + 1,  captionText.value, captionColor.value);
            graph.drawGraph();
        }
    }
});