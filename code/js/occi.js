/*
 * occi.js Open Cloud Computing Interface (OCCI) Javascript Client Library
 * 
 * Copyright 2009 Mike Kelly <mike@mykanjo.co.uk>
 *                Sam Johnston <samj@samj.net>
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * 
 * CHANGELOG
 * 2009-10-28 Initial release
 * 
 * TODO
 * - consider adding support for loadable modules ala google.load()
 *   http://my.opera.com/kilsmo/blog/2009/07/11/libraries-in-javascript
 */
var occi = {}; 
 
occi.uri = document.location.href; 
occi.xhr = null; 

if (window.XMLHttpRequest) { 
    // code for Firefox, Mozilla, IE7, etc. 
      occi.xhr = new XMLHttpRequest(); 
} else if (window.ActiveXObject) { 
    // code for IE6, IE5 
      occi.xhr = new ActiveXObject("Microsoft.XMLHTTP"); 
} 

occi.test = function() {
    if (occi.xhr!=null) { 
        occi.xhr.onreadystatechange = function() { 
            if(occi.xhr.readyState == 4) { 
                x = occi.xhr.getAllResponseHeaders(); 
                document.getElementById("header").innerHTML = x; 
            } 
        } 
        occi.xhr.open("HEAD",occi.URI, true);
        occi.xhr.send(); 
    } else { 
        alert("Your browser does not support XMLHTTP."); 
    }
}

occi.open = function(method, uri, headers, callback) {
	method = method || 'GET';
	if (occi.xhr!=null) { 
        occi.xhr.onreadystatechange = function() { 
            if(occi.xhr.readyState == 4) { 
                callback();
            } 
        } 
        // TODO: catch error for unsupported method and use override
        occi.xhr.open(method, uri, true);
        occi.xhr.setReqeustHeader('X-HTTP-Method-Override', method);
        // TODO: foreach header
        for (var h in headers) {
		   occi.xhr.setReqeustHeader(h, headers[h]);
		}
        occi.xhr.send(); 
    } else { 
        alert("Your browser does not support XMLHTTP."); 
    }
}

occi.copy = function(src, dst, callback) {
	occi.open()
	if (occi.xhr!=null) { 
        occi.xhr.onreadystatechange = function() { 
            if(occi.xhr.readyState == 4) { 
                callback();
            } 
        } 
        occi.xhr.open('COPY', src, true);
        occi.xhr.setReqeustHeader('X-HTTP-Method-Override', 'COPY');
        occi.xhr.setReqeustHeader('Destination', dst);
        occi.xhr.send(); 
    } else { 
        alert("Your browser does not support XMLHTTP."); 
    }
}

occi.move = function(src, dst, callback) {
	occi.open()
	if (occi.xhr!=null) { 
        occi.xhr.onreadystatechange = function() { 
            if(occi.xhr.readyState == 4) { 
                callback();
            } 
        } 
        occi.xhr.open('MOVE', src, true);
        occi.xhr.setReqeustHeader('X-HTTP-Method-Override', 'MOVE');
        occi.xhr.setReqeustHeader('Destination', dst);
        occi.xhr.send(); 
    } else { 
        alert("Your browser does not support XMLHTTP."); 
    }
}
