(function ($) {
    $(window).on('map:init', function (e) {
        var detail = e.originalEvent ? e.originalEvent.detail : e.detail;
        var map = detail.map;
        
        //Fulscreen map button
        map.addControl(new L.Control.Fullscreen());
        
        //Adding the sidebar to the map
        //Adds the HTML div with id="sidebar" from map.html to the map
        var sidebar = L.control.sidebar({ container: 'sidebar', closeButton: false, position: 'right'}).addTo(map);
        
        // TODO: Some kind of loading indicator
        
        //Time selection for the recently offline nodes
        //Currently it is 24h since now-1h
        var time_start = new Date();
        var time_stop = new Date();
        time_start.setHours(time_start.getHours() - 25);
        time_stop.setHours(time_stop.getHours() - 1);
        
        //APIv2 request for the recently offline nodes
        $.ajax({
            'url': '/api/v2/node/?format=json&limit=1&&filters=monitoring:core.general__last_seen__gt="' + time_start.toISOString() + '",monitoring:core.general__last_seen__lt="' + time_stop.toISOString() + '"',
        }).done(function(data) {
            for(var i = 1; i < data.count; i++) {
                $.ajax({
                    'url': '/api/v2/node/?format=json&limit=1&fields=monitoring:core.general__last_seen&fields=config:core.location&fields=config:core.general&fields=config:core.type&filters=monitoring:core.general__last_seen__gt="' + time_start.toISOString() + '",monitoring:core.general__last_seen__lt="' + time_stop.toISOString() + '"&offset=' + (i - 1),
                }).done(function(data) {
                    var node = {
                        'data': {
                            'n': data.results[0]["config"]["core.general"]["name"],                         //node name
                            'i': data.results[0]["@id"],                                                    //node id
                            't': data.results[0]["config"]["core.type"]["type"],                            //node type
                            'l': (data.results[0]["config"]["core.location"]["geolocation"] ? data.results[0]["config"]["core.location"]["geolocation"]["coordinates"] : null),  //node coordinates
                            'api': "v2",                                                                    //api version which was used to get the data
                        },
                    }
                    sidebarTableAddNode(node,"recently-offline-table");
                });
            }
        });
        
        // Function to load nodes from API v2 (fallback when no topology data)
        function loadNodesFromAPIv2(map) {
            $.ajax({
                'url': '/api/v2/node/?format=json&limit=100',
            }).done(function(data) {
                if (data.count === 0) return;

                var nodes = [];
                var nodeIndex = {};
                var loadedCount = 0;

                // Load each node's details
                $.each(data.results, function(index, result) {
                    $.ajax({
                        'url': '/api/v2/node/' + result['@id'] + '/?format=json&fields=config:core.location,config:core.general,config:core.type',
                    }).done(function(nodeData) {
                        var loc = nodeData['config'] && nodeData['config']['core.location'] && nodeData['config']['core.location']['geolocation'];
                        var general = nodeData['config'] && nodeData['config']['core.general'];
                        var nodeType = nodeData['config'] && nodeData['config']['core.type'];

                        if (loc && loc.coordinates) {
                            nodes.push({
                                'index': nodes.length,
                                'data': {
                                    'n': general ? general.name : 'Unknown',
                                    'i': result['@id'],
                                    't': nodeType ? nodeType.type : 'unknown',
                                    'l': loc.coordinates,
                                    'api': 'v2'
                                }
                            });
                        }

                        loadedCount++;
                        if (loadedCount >= data.results.length) {
                            // All nodes loaded, extend the map
                            $.nodewatcher.map.extend(map, nodes, []);
                        }
                    }).fail(function() {
                        loadedCount++;
                        if (loadedCount >= data.results.length) {
                            $.nodewatcher.map.extend(map, nodes, []);
                        }
                    });
                });
            });
        }

        //APIv1 request for all the currently active nodes with the location parameter set
        $.ajax({
            'url': "/api/v1/stream/?format=json&tags__module=topology&limit=1",
        }).done(function(data) {
            // Check if we have topology data
            if (!data.objects || data.objects.length === 0) {
                // No topology data, fall back to API v2
                loadNodesFromAPIv2(map);
                return;
            }

            var streamId = data.objects[0].id;
            var latestTimestamp = moment(data.objects[0].latest_datapoint).unix();
            $.ajax({
                'url': "/api/v1/stream/" + streamId + "/?format=json&reverse=true&limit=1&start=" + latestTimestamp,
            }).done(function(data) {
                if (!data.datapoints || data.datapoints.length === 0) {
                    // No datapoints, fall back to API v2
                    loadNodesFromAPIv2(map);
                    return;
                }

                var graph = data.datapoints[0].v;
                var nodes = [];
                var edges = [];
                var nodeIndex = {};

                //storing each node data
                $.each(graph.v, function(index, vertex) {
                    nodes.push({
                        'index': index,     //index of the node
                        'data': vertex,     //data which stores the name, id, type and coordinates
                    });
                    nodeIndex[vertex.i] = index;
                });

                //storing the links between the nodes
                $.each(graph.e, function(index, edge) {
                    edges.push({
                        'source': nodeIndex[edge.f],
                        'target': nodeIndex[edge.t],
                        'data': edge,
                    });
                });

                $.nodewatcher.map.extend(map, nodes, edges);
            }).fail(function() {
                // API call failed, fall back to API v2
                loadNodesFromAPIv2(map);
            });
        }).fail(function() {
            // API call failed, fall back to API v2
            loadNodesFromAPIv2(map);
        });
    });
})(jQuery);
