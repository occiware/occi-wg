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
var OCCIclient = {}; 
 
OCCIclient.URI = document.location.href; 
OCCIclient.XHR = null; 
 
if (window.XMLHttpRequest) { 
    // code for Firefox, Mozilla, IE7, etc. 
      OCCIclient.XHR = new XMLHttpRequest(); 
} else if (window.ActiveXObject) { 
    // code for IE6, IE5 
      OCCIclient.XHR = new ActiveXObject("Microsoft.XMLHTTP"); 
} 

if (OCCIclient.XHR!=null) { 
    OCCIclient.XHR.onreadystatechange = function() { 
        if(OCCIclient.XHR.readyState == 4) { 
              x = OCCIclient.XHR.getAllResponseHeaders(); 
             document.getElementById("header").innerHTML = x; 
          } 
    } 
    OCCIclient.XHR.open("HEAD",OCCIclient.URI, true); 
    OCCIclient.XHR.send(); 
} else { 
    alert("Your browser does not support XMLHTTP."); 
}
