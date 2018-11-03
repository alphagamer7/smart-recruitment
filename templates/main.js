        //reload for matplotlib pie chart
        if (!localStorage.getItem("reload")) {
            localStorage.setItem("reload", "true");
            location.reload();
        }
        else {
            localStorage.removeItem("reload");
        }

        //add image
        document.getElementById('image').src = "https://twitter.com/"+new URL(window.location.href).searchParams.get("profile_name")+"/profile_image?size=bigger";

        // variables
        let vWidth = 650;
        let vHeight = 650;
        let vRadius = Math.min(vWidth, vHeight) / 2;
        let vColor = d3.scaleOrdinal(d3.schemeCategory20);


        // Size our <svg> element, add a <g> element, and move translate 0,0 to the center of the element.
        let g = d3.select('svg')
            .attr('width', vWidth)
            .attr('height', vHeight)
            .append('g')
            .attr('transform', 'translate(' + vWidth / 2 + ',' + vHeight / 2 + ')');

        // Create our sunburst data structure and size it.
        let partition = d3.partition()
            .size([2 * Math.PI, vRadius]);

        // Get the data from our JSON file
        d3.json("{{ url_for('static', filename='data-intermediate.json') }}", function (error, nodeData) {
            if (error) throw error;

            drawSunburst(nodeData);
        });

        function drawSunburst(data) {

            // Find the root node, calculate the node.value, and sort our nodes by node.value
            root = d3.hierarchy(data)
                .sum(function (d) {
                    return d.size;
                })
                .sort(function (a, b) {
                    return b.value - a.value;
                });

            // Calculate the size of each arc; save the initial angles for tweening.
            partition(root);
            arc = d3.arc()
                .startAngle(function (d) {
                    d.x0s = d.x0;
                    return d.x0;
                })
                .endAngle(function (d) {
                    d.x1s = d.x1;
                    return d.x1;
                })
                .innerRadius(function (d) {
                    return d.y0;
                })
                .outerRadius(function (d) {
                    return d.y1;
                });

            // Add a <g> element for each node; create the slice letiable since we'll refer to this selection many times
            let slice = g.selectAll('g.node').data(root.descendants(), function (d) {
                return d.data.id;
            });
            newSlice = slice.enter().append('g').attr('class', 'node').merge(slice);
            slice.exit().remove();

            // Append <path> elements and draw lines based on the arc calculations. Last, color the lines and the slices.
            slice.selectAll('path').remove();
            newSlice.append('path').attr('display', function (d) {
                return d.depth ? null : 'none';
            })
                .attr('d', arc)
                .style('stroke', '#fff')
                .style('fill', function (d) {
                    return vColor((d.children ? d : d.parent).data.id);
                });

            // Populate the <text> elements with our data-driven titles.
            slice.selectAll('text').remove();
            newSlice.append('text')
                .attr('transform', function (d) {
                    return 'translate(' + arc.centroid(d) + ')rotate(' + computeTextRotation(d) + ')';
                })
                .attr('dx', '-20')
                .attr('dy', '.5em')
                .text(function (d) {
                    return d.parent ? d.data.id : ''
                })
                .style("font-size","12px");

            newSlice.on('click', highlightSelectedSlice);
        }

        var svg =d3.select('svg');

        var defs = svg.append("defs").attr("id", "imgdefs")

        var clipPath = defs.append('clipPath').attr('id', 'clip-circle')
        .append("circle")
        .attr("r", 110)
        .attr("cy", 110)
        .attr("cx", 110);


        var username = new URL(window.location.href).searchParams.get("profile_name");

        svg.append("image").attr("xlink:href", `https://twitter.com/${username}/profile_image?size=bigger`)
        .attr("width", 220).attr("height", 220)
        .attr("transform", "translate(" + 215 + "," + 215 + ")").attr("clip-path", "url(#clip-circle)")


        d3.selectAll('.sizeSelect').on('click', sliceSizer);

        function highlightSelectedSlice(clicked) {

            let rootPath = clicked.path(root).reverse();  // finds the path from between 2 points and reverses it
            rootPath.shift(); // remove root node from the array

            newSlice.style('opacity', 0.4);  // sets the entire sunburst to 40% opacity
            newSlice.filter(function (d) {   // cycle through and test each node (d will be a diff node each iteration)
                if (d === clicked && d.prevClicked) {  // if d is the clicked node this time, and it was the clicked node...
                    d.prevClicked = false;   // ...last time, then reset sunburst to starting point, and add this node to...
                    newSlice.style('opacity', 1);  // ...the filter
                    return true;

                } else if (d === clicked) {  // if d is the clicked node, but it wasn't previously clicked, then remember...
                    d.prevClicked = true;  // ...it for next time and add it to the filter
                    return true;
                } else {
                    d.prevClicked = false;  // this isn't a clicked node, so just check to see if it's part of our...
                    return (rootPath.indexOf(d) >= 0);  // rootPath--if so, then keep it in the filter
                }
            })
                .style('opacity', 1);  // all nodes that made it through the filter have opacity set to full
        }

        function sliceSizer() {

            // Determine how to size the slices.
            if (this.value === 'size') {
                root.sum(function (d) {
                    return d.size;
                });
            } else if (this.value === 'top3') {
                // Create "topSize" letiable to store the size (0 or actual) based on user selection. Return it to d3.sum.
                root.sum(function (d) {
                    d.topSize = ((d.rank <= 3) ? d.size : 0);
                    return d.topSize;
                });
            } else {
                root.count();
            }
            root.sort(function (a, b) {
                return b.value - a.value;
            });

            partition(root);

            newSlice.selectAll('path').transition().duration(750).attrTween('d', arcTweenPath);
            newSlice.selectAll('text').transition().duration(750).attrTween('transform', arcTweenText)
                .attr("opacity", function (d) {
                    return d.x1 - d.x0 > 0.06 ? 1 : 0;
                });
        }

        function arcTweenPath(a) {

            let oi = d3.interpolate({x0: a.x0s, x1: a.x1s}, a);

            function tween(t) {
                let b = oi(t);
                a.x0s = b.x0;
                a.x1s = b.x1;
                return arc(b);
            }

            return tween;
        }

        function arcTweenText(a) {

            let oi = d3.interpolate({x0: a.x0s, x1: a.x1s}, a);

            function tween(t) {
                let b = oi(t);
                return 'translate(' + arc.centroid(b) + ')rotate(' + computeTextRotation(b) + ')';
            }

            return tween;
        }

        function computeTextRotation(d) {
            let angle = (d.x0 + d.x1) / Math.PI * 90;

            // Avoid upside-down labels
            return (angle < 120 || angle > 270) ? angle : angle + 180;  // labels as rims
            //return (angle < 180) ? angle - 90 : angle + 90;  // labels as spokes
        }