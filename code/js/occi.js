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
 * Authors: 
 *          
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

occi.open = function(uri, method) {
	method = method || 'GET';
	if (occi.xhr!=null) { 
        occi.xhr.onreadystatechange = function() { 
            if(occi.xhr.readyState == 4) { 
                // do something with the xhr
            } 
        } 
        occi.xhr.open(method, uri, true); 
        occi.xhr.send(); 
    } else { 
        alert("Your browser does not support XMLHTTP."); 
    }
}
