function toggleButtonSwitch(relay, switchid) {
  var switchButton = document.getElementById(switchid);
  
  var toggleValue = "";
  if (switchButton.checked) {
    console.log("On!");
    toggleValue = "ON";
  } else {
    console.log("Off!");
    toggleValue = "OFF"
  }
  fetch( `/toggle/`+relay)
  .then( response => {
    console.log(response);
  } )
}

function updateStates() {
  const switches = document.querySelectorAll('[id^="switch-"]');
  switches.forEach(el => {
    const relay = el.id.split("-")[1];
    fetch("/state/"+relay)
    .then(r => r.json()).then( s => {
      if (s["val"] == 1) {
        el.switchButton('on', true);
      } else {
        el.switchButton('off', true);
      }
    } )
  })
}

setInterval(function() {
  // catch all the errors.
  updateStates()
}, 1000*30);