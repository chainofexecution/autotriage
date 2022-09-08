const randNum = Math.floor(Math.random() * (3 - 1) + 1)
console.log("Generated Random Number: " + randNum)
switch("" + randNum) { // Give us a random meme.
  case "1":
    console.log("Case used: " + randNum)
    document.getElementById("gif").innerHTML = "<img src=\"waiting1.gif\" />";
    break;
  case "2":
    document.getElementById("gif").innerHTML = "<img src=\"waiting2.gif\" width=\"400px\"/>";
      console.log("Case used: " + randNum)
    break;
  case "3":
    document.getElementById("gif").innerHTML = "<img src=\"waiting3.gif\" />";
      console.log("Case used: " + randNum)
    break;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function demo() {
  for (let i = 0; i < 300; i++) { // Loop for 300 seconds.
      await sleep(1000);
      document.getElementById("timeElapsed").innerHTML = "You have been waiting for " + (i + 1) + " seconds.";
  }
}

demo();
