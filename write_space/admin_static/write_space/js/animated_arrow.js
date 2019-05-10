



function first(first_count,array_item){
  var first =(first_count*100)/first_count;
  console.log(first);
  $(array_item+".progress-bar.progress-bar-success.first").css("width",first+"%").attr("aria-valuenow",first);
}

function second(first_count,second_count,array_item){
  var second =(second_count*100)/first_count;
  console.log(second);
  $(array_item+".progress-bar.progress-bar-success.second").css("width",second+"%").attr("aria-valuenow",second);
}

function third(first_count,third_count,array_item){
  var third =(third_count*100)/first_count;
  console.log(third);
  $(array_item+".progress-bar.progress-bar-success.third").css("width",third+"%").attr("aria-valuenow",third);
}


function genesis(){
  var arr = ["#first_vote","#second_vote","#third_vote"];
  for(i=0;i<arr.length;i++){
    var first_count = document.querySelector(arr[i]).querySelector(".poll_card__vote_count_number_first").textContent;
    var second_count = document.querySelector(arr[i]).querySelector(".poll_card__vote_count_number_second").textContent;
    var third_count = document.querySelector(arr[i]).querySelector(".poll_card__vote_count_number_third").textContent;

    first(first_count,arr[i]);
    second(first_count,second_count,arr[i]);
    third(first_count,third_count,arr[i]);
  }
}

genesis();
