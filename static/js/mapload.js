
var url = window.location.href + 'propiedades'

$.get(url, function(list) {
	
	map = new OpenLayers.Map("mapdiv");
	map.addLayer(new OpenLayers.Layer.OSM());
	
	epsg4326 =  new OpenLayers.Projection("EPSG:4326"); //WGS 1984 projection
	projectTo = map.getProjectionObject(); //The map projection (Spherical Mercator)
   
	var vectorLayer = new OpenLayers.Layer.Vector("Overlay");
	
			
	propiedades = JSON.parse(list);		
	size = Object.keys(propiedades['precio']).length;
	
	var center_lat = -34.556961;
	var center_lon = -58.495059;
	var zoom = 13;
	
	for(var i= 0; i < size; i++)
	{
		lat = propiedades['latitud'][i];
		lon = propiedades['longitud'][i];
		titulo = propiedades['titulo'][i];
		ambientes = propiedades['ambientes'][i];
		m2 = propiedades['m2'][i];
		marca = propiedades['marca'][i];
		moneda = '$'
		
		if(propiedades['moneda'][i] == 'USD')
		{
			moneda = 'us$'
		}
		if(ambientes == '')
		{
			ambientes = '-'
		}
		if(m2 == '')
		{
			m2 = '-'
		}
		precio = moneda + propiedades['precio'][i];
	
		msj = titulo + '<br>' + '<b>' + precio + '</b>' + '<br>' + 'Ambientes: ' + ambientes + ', superficio[m2]: ' + m2
	
		if(i == 0)
		{
			//center_lat = lat;
			//center_lon = lon;
		}
		
		
		var feature = new OpenLayers.Feature.Vector(
			new OpenLayers.Geometry.Point(lon, lat ).transform(epsg4326, projectTo),
			{description: msj} ,
			{externalGraphic: marca, graphicHeight: 25, graphicWidth: 21, graphicXOffset:-12, graphicYOffset:-25  }
		);    
		vectorLayer.addFeatures(feature);
	}   
		
	var lonLat = new OpenLayers.LonLat( center_lon, center_lat ).transform(epsg4326, projectTo);        
	map.setCenter (lonLat, zoom);
	   
	map.addLayer(vectorLayer);
 
	
	//Add a selector control to the vectorLayer with popup functions
	var controls = {
	  selector: new OpenLayers.Control.SelectFeature(vectorLayer, { onSelect: createPopup, onUnselect: destroyPopup })
	};

	function createPopup(feature) {
	  feature.popup = new OpenLayers.Popup.FramedCloud("pop",
		  feature.geometry.getBounds().getCenterLonLat(),
		  null,
		  '<div class="markerContent">'+feature.attributes.description+'</div>',
		  null,
		  true,
		  function() { controls['selector'].unselectAll(); }
	  );
	  //feature.popup.closeOnMove = true;
	  map.addPopup(feature.popup);
	}

	function destroyPopup(feature) {
	  feature.popup.destroy();
	  feature.popup = null;
	}
	
	map.addControl(controls['selector']);
	controls['selector'].activate();
	

}); 

      
