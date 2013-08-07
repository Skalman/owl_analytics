;(function() {

	// helper method to generate a color from a cycle of colors.
	var curColourIndex = 1, maxColourIndex = 24, nextColour = function() {
		var R,G,B;
		R = parseInt(128+Math.sin((curColourIndex*3+0)*1.3)*128);
		G = parseInt(128+Math.sin((curColourIndex*3+1)*1.3)*128);
		B = parseInt(128+Math.sin((curColourIndex*3+2)*1.3)*128);
		curColourIndex = curColourIndex + 1;
		if (curColourIndex > maxColourIndex) curColourIndex = 1;
		return "rgb(" + R + "," + G + "," + B + ")";
	 };	
		
	window.jsPlumbDemo = { 
	
		init :function() {

			var seq = new Typed_sequence(conf);
			// var seq = new Sequence(conf);
			window.seq = seq;
			window.do_layout = do_layout;

			var i = 0;
			$.each(seq.blocks, function (id, block) {
				$('<div>', {'class':'w', id: id, text: id, css: {top:(++i*4)+'em', left:'2em'}})
					.append($('<div>', {'class':'ep'}))
					.appendTo('#main');
			});

			// setup some defaults for jsPlumb.	
			jsPlumb.importDefaults({
				Endpoint : ["Dot", {radius:2}],
				HoverPaintStyle : {strokeStyle:"#42a62c", lineWidth:2 },
				ConnectionOverlays : [
					[ "Arrow", { 
						location:-4,
						id:"arrow",
						length:14,
						foldback:0.8
					} ],
					// [ "Label", { label:"FOO", id:"label" }]
				]
			});

						// initialise draggable elements.  
			jsPlumb.draggable($(".w"));

						// bind a click listener to each connection; the connection is deleted. you could of course
			// just do this: jsPlumb.bind("click", jsPlumb.detach), but I wanted to make it clear what was
			// happening.
			jsPlumb.bind("click", function(c) { 
				seq.delete_edge(c.id);
				jsPlumb.detach(c);
				do_layout();
				console.log( 'deleting... %s', c.id, seq );
			});
				
			// make each ".ep" div a source and give it some parameters to work with.  here we tell it
			// to use a Continuous anchor and the StateMachine connectors, and also we give it the
			// connector's paint style.  note that in this demo the strokeStyle is dynamically generated,
			// which prevents us from just setting a jsPlumb.Defaults.PaintStyle.  but that is what i
			// would recommend you do. Note also here that we use the 'filter' option to tell jsPlumb
			// which parts of the element should actually respond to a drag start.


			$(".w").each(function(i,e) {			
				jsPlumb.makeSource(e, {
					filter:".ep",
					anchor:"Continuous",
					// connector:[ "StateMachine", { curviness:20 } ],
					connector:[ "Flowchart", { cornerRadius:5 } ],
					connectorStyle:{ strokeStyle:'#666', lineWidth:2 },
					// maxConnections:-1,
					onMaxConnections:function(info, e) {
						alert("Maximum connections (" + info.maxConnections + ") reached");
					}
				});
			});


			// bind a connection listener. note that the parameter passed to this function contains more than
			// just the new connection - see the documentation for a full list of what is included in 'info'.
			// this listener changes the paint style to some random new color and also sets the connection's internal
			// id as the label overlay's text.
			jsPlumb.bind("connection", function(info) {
				try {
					console.log( info );
					seq.set_edge({
						id: info.connection.id,
						from: info.connection.getParameter('from'),
						to: info.connection.getParameter('to')
					});
					do_layout();
				} catch (e) {
					console.log( 'could not set edge (msg: %s) - removing again', e.message, e.stack );
					if (!jsPlumb.detach(info.connection)) {
						console.error('failed to remove connection!!!');
					}
				}
			});

			// initialise all '.w' elements as connection targets.
			jsPlumb.makeTarget($(".w"), {
				dropOptions:{ hoverClass:"dragHover" },
				anchor:"Continuous"				
			});
			
			// and finally, make a couple of connections
			var edges = seq.edges;
			seq.edges = {};
			$.each(edges, function (id, edge) {
				console.log( 'connect ', edge.from.block, '->', edge.to.block );
				var connection = jsPlumb.connect({
					source: edge.from.block,
					target: edge.to.block,
					parameters: {
						from: edge.from,
						to: edge.to
					}
				});
				// jsPlumb.connect(connection);
				// edge.id = connection.id;
				// seq.set_edge(edge);
			});

			function do_layout() {
				try {
					var layout = seq.sort_blocks();
					$.each(layout, function (id, block_pos) {
						$('#'+id).css({
							top: (5+6*block_pos.branch) + 'em',
							left: (15*block_pos.time) + 'em'
						})
					});
				} catch (e) {
					console.error( 'tried and failed to sort blocks', e.stack );
				}

				setTimeout(jsPlumb.repaintEverything, 40);
				setTimeout(jsPlumb.repaintEverything, 80);
				setTimeout(jsPlumb.repaintEverything, 120);
				setTimeout(jsPlumb.repaintEverything, 160);
				setTimeout(jsPlumb.repaintEverything, 200);
			}


		}
	};
})();


/*
 *  This code below contains the JS that handles the first init of each jQuery demonstration, and also switching
 *  between render modes.
 */
jsPlumb.bind("ready", function() {

	// chrome fix.
	document.onselectstart = function () { return false; };				

    // render mode
	var resetRenderMode = function(desiredMode) {
		var newMode = jsPlumb.setRenderMode(desiredMode);
		$(".rmode").removeClass("selected");
		$(".rmode[mode='" + newMode + "']").addClass("selected");		

		$(".rmode[mode='canvas']").attr("disabled", !jsPlumb.isCanvasAvailable());
		$(".rmode[mode='svg']").attr("disabled", !jsPlumb.isSVGAvailable());
		$(".rmode[mode='vml']").attr("disabled", !jsPlumb.isVMLAvailable());
					
		jsPlumbDemo.init();
	};
     
	$(".rmode").bind("click", function() {
		var desiredMode = $(this).attr("mode");
		if (jsPlumbDemo.reset) jsPlumbDemo.reset();
		jsPlumb.reset();
		resetRenderMode(desiredMode);					
	});	

	resetRenderMode(jsPlumb.SVG);
       
});
