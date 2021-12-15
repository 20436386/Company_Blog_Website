// document.addEventListener("mouseup", getSelectedText)

// function getSelectedText(){
//     selection = window.getSelection().toString();
//     console.log(selection)
    
// }

// $(document).ready(function () {
//     function tweetButtonClick() {
//       let selectedText = document.getSelection().toString();
//       /*window.open(
//         "https://twitter.com/intent/tweet?url=https://www.linkedin.com/in/harsha-vardhan-ch-245197bb/&text=" +
//           selectedText
//       );*/
//       console.log("This is your selected text: ",selectedText);
//     }
  
//     const textSelectionTooltipContainer = document.createElement("div");
//     textSelectionTooltipContainer.setAttribute(
//       "id",
//       "textSelectionTooltipContainer"
//     );
//     textSelectionTooltipContainer.innerHTML = `<button id="textShareTwitterBtn">TWEET</button>`;
//     const bodyElement = document.getElementsByTagName("BODY")[0];
  
//     $("body").on("click", "#textShareTwitterBtn", tweetButtonClick);
  
//     bodyElement.addEventListener("mouseup", function (e) {
//       var textu = document.getSelection().toString();
//       if (!textu.length) {
//         textSelectionTooltipContainer.remove();
//       }
//     });
  
//     document.getElementById("textToSelect").addEventListener("mouseup", function (e) {
//         let textu = document.getSelection().toString();
//         let matchu = /\r|\n/.exec(textu);
//         if (textu.length && !matchu) {
//           let range = document.getSelection().getRangeAt(0);
//           rect = range.getBoundingClientRect();
//           scrollPosition = $(window).scrollTop();
//           containerTop = scrollPosition + rect.top - 50 + "px";
//           containerLeft = rect.left + rect.width / 2 - 50 + "px";
//           textSelectionTooltipContainer.style.transform =
//             "translate3d(" + containerLeft + "," + containerTop + "," + "0px)";
//           bodyElement.appendChild(textSelectionTooltipContainer);
//         }
//       });
//   });

$(document).ready(function (){
    //Define new element. This element will represent the tooltip container/popup block.
    const textSelectionTooltipContainer = document.createElement("div");
    textSelectionTooltipContainer.setAttribute("id", "textSelectionTooltipContainer");
    //Add button to the new container
    textSelectionTooltipContainer.innerHTML = '<button id="textSelectionBold"><strong>B</strong></button> <button id="textSelectionEm"><em>I</em></button> <button id="textSelectionUnderline"><u>U</u></button> <button id="textSelectionLink">#</button> <button id="textSelectionH2"><strong>H2</strong></button> <button id="textSelectionH3"><strong>H3</strong></button> <button id="textSelectionButton">"</button>'
    
    //Define variable that will hold element containing selected text - dont need this
    // anchorElement = document.getSelection().anchorNode.parentElement
    // console.log(anchorElement)
    
    
    //Call relevant function when button is clicked
    // $("body").on("click", "#textSelectionBold", textSelectionBold)
    // $("body").on("click", "#textSelectionEm", textSelectionEm)
    // $("body").on("click", "#textSelectionUnderline", textSelectionUnderline)
    // $("body").on("click", "#textSelectionLink", textSelectionLink)
    // $("body").on("click", "#textSelectionH2", textSelectionH2)
    // $("body").on("click", "#textSelectionH3", textSelectionH3)



    //Get body element
    const bodyElement = document.getElementsByTagName("body")[0];
    // console.log(bodyElement)

    //Will remove the tooltip object if it exists, when user clicks anywhere on the page
    $("body").on("mouseup", function(){
        var text = document.getSelection().toString();
        //Note:Can have more than one selection on screen i.e. using ctl, '.rangecount' will return number of selections 
        // console.log(document.getSelection());
        if(text.length == 0){
            // console.log("text length = 0")
            tooltipObject = document.getElementById("textSelectionTooltipContainer");
            // console.log("tooltipObject = " + tooltipObject)
            if (tooltipObject != null){
                // console.log("remove")
                tooltipObject.remove();
            }
        }
    })

    //<button id="textSelectionButton"><strong>H3</strong></button>
    //element.innerHTML = element.innerHTML.replace(document.getSelection().toString(), "<em>new</em>")

    //On mouseup get bounding box of selected text and use it set position of textselectiontooltipcontainer
    $(".selectable").on("mouseup", function(){
        var text = document.getSelection().toString();
        // console.log(text)
        // console.log(text.length)
        if (text.length > 0){
            var range = document.getSelection().getRangeAt(0); //returns a range object representing one of the ranges currently selected. 
            var rect = range.getBoundingClientRect(); // The returned value is a DOMRect object which is the smallest rectangle which contains the entire element, including its padding and border-width. The left, top, right, bottom, x, y, width, and height properties describe the position and size of the overall rectangle in pixels. Properties other than width and height are relative to the top-left of the viewport. 
            var scrollPosition = $(window).scrollTop() //Gets the number of pixels an element's content is scrolled horizontally
            //Set the position of the textselectiontooltipcontainer
            containerTop = scrollPosition + rect.top - 40 + "px";
            containerLeft = rect.left + rect.width/2 - 100 + "px";
            // textSelectionTooltipContainer.style.transform = "translate3d(containerLeft, containerTop, 0px)";
            transform = "translate3d(" + containerLeft + "," + containerTop + "," + "0px)"; 
            textSelectionTooltipContainer.style.transform = transform
            //Have to append the element to the body object
            bodyElement.appendChild(textSelectionTooltipContainer)
        }
    })

    // //Button functions
    // function textSelectionBold(){

    // }
})