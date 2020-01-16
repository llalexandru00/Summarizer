var bns = document.getElementsByTagName("button");

for (var i = 0; i < bns.length; i++) 
{
    bns[i].addEventListener("click", function(e) {
        var target = e.originalTarget.name;
        var input = document.getElementById(target);
        console.log(target);
        if (input.classList.contains("out"))
        {
            input.classList.remove("out");
            input.value = input.value.substr(0, input.value.length - 7);    
        }
        else
        {
            input.classList.add("out");
            input.value = input.value + " <<out>>";
        }
    });
}