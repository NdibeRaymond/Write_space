
(function main(){
  console.log(" i am old on this block");

  function commentBox(){
    let commentForm = document.querySelector(".comment-form");
    let commentText = document.querySelector(".comment-text");
    let commentAuthorName = document.querySelector(".comment-form .comment_meta__a");
    let commentPublishButton = document.querySelector(".comment-publish-button");
    if(commentForm){
      commentText.addEventListener("focus",()=>{
        commentForm.classList.remove("comment-collapsed");
        commentForm.classList.add("comment");
        commentAuthorName.classList.remove("display-none");
        commentPublishButton.classList.remove("display-none");
      })

      document.addEventListener("click",e=>{
        if(![commentForm,commentPublishButton,commentText].includes(e.target)){
        commentForm.classList.remove("comment");
        commentForm.classList.add("comment-collapsed");
        commentAuthorName.classList.add("display-none");
        commentPublishButton.classList.add("display-none");
       }
      })
    }
  }




    function summerNote(){
      let summernoteMedia = "summernote_media";
      let cloudName = "raymondndibe";

      function sendFile(file){
        console.log("in sendfile");
        data = new FormData();
        data.append("file",file);
        data.append("upload_preset",summernoteMedia);
        $.ajax({
          url:`https://api.cloudinary.com/v1_1/${cloudName}/upload`,
          data: data,
          cache: false,
          contentType: false,
          processData: false,
          type: "POST",
          success: function(data){
            console.log("transfer was succesful.......");
            let imgNode = document.createElement("img");
            var iframe = $('iframe');
            imgNode.setAttribute('src', data.secure_url);
            imgNode.setAttribute("style","max-width:100%;height:auto")
          $(".note-editable", iframe.contents()).append(imgNode);
          },
          error: function(jqXHR, textStatus, errorThrown){
            alert(textStatus+" "+errorThrown)
          }
        })
      };

      let mObserver = "";

      let mutationOptions = {
        childList: true,
        subtree: false,
      };

      let mCallback = (mutations) =>{
        for(let mutation in mutations){
          if(mutations[mutation].removedNodes.length > 0
          && mutations[mutation].removedNodes[0].src !== null
          && mutations[mutation].removedNodes[0].src !== undefined){
            makeDeleteRequest("post_image_pic",mutations[mutation].removedNodes[0].src)
            .then(result=>{
              if(result["result"] === "ok"){
                console.log("image was deleted successfully")
              }
            })
          }
        }
      };

      let t0 = performance.now();

      let overRideOnImageUpload = setInterval(()=>{
        if(window.settings_id_text !== undefined
          && window.settings_id_text.callbacks !== undefined
          && window.settings_id_text.callbacks.onImageUpload !== null){
          console.log("no longer null");
          window.settings_id_text.callbacks.onImageUpload = function(files){
            sendFile(files[0])
          }
          let iframe = document.querySelector('iframe');
          let innerDoc = iframe.contentDocument || iframe.contentWindow.document;
          // let iframe = $('iframe');
          // let targetElement = $(".note-editable", iframe.contents());
          let targetElement = innerDoc.querySelector(".note-editable");
          let observer = new MutationObserver(mCallback);
          observer.observe(targetElement,mutationOptions);
        clear();
        };
        if((performance.now() - t0) > 10000){
          clear()
        }
      },1000);

      function clear(){
        clearInterval(overRideOnImageUpload)
      }
    }

    commentBox();
    summerNote();

  }())

  cloudinary.setCloudName("raymondndibe");

  let generateSignature = function(callback, params_to_sign){
    $.ajax({
     url     : "https://www.my-domain.com/my_generate_signature",
     type    : "GET",
     dataType: "text",
     data    : { data: params_to_sign},
     complete: function() {console.log("complete")},
     success : function(signature, textStatus, xhr) { callback(signature); },
     error   : function(xhr, status, error) { console.log(xhr, status, error); }
    });
  }

  // ###################################################################

  function removeElement(elem){
    console.log("removeElement was called");
    if(elem){
    elem.parentNode.removeChild(elem);
    }
  }

  function checkResponse(result,img_func){
    if(result["result"] === "ok"){
      console.log("delete was successful");
      let thumbnail = document.querySelector(`.${img_func}_thumbnail`);
      let cloudinary_thumbnails = document.querySelector(`.${img_func}_thumbnails .cloudinary-thumbnails`);
      let hidden_field = document.querySelector(`.user_pic_form [name="${img_func}_url"]`);
      return [thumbnail,cloudinary_thumbnails,hidden_field]
    }
  }

  function makeDeleteRequest(img_func,urlToDelete){
    let elem = document.querySelector("#user_identity");
    let username = elem.getAttribute("username");
    let pk = elem.getAttribute("pk");
    let prev_url = null;
    let current_url = null;

    if(img_func === "profile_pic" || img_func === "background_pic"){

    prev_url = document.querySelector(`.${img_func}_thumbnail`);
    current_url = document.querySelector(`.${img_func}_thumbnails .cloudinary-thumbnail`);
    prev_url = prev_url ? prev_url.getAttribute("src") : null;
    current_url = current_url ? JSON.parse(current_url.getAttribute("data-cloudinary"))["secure_url"] : null;

    }else if(img_func === "post_image_pic"){
    prev_url = urlToDelete;
    }

    if(prev_url || current_url){
      let url = prev_url ? prev_url : current_url;
      url = url.split(".")[2].split("/");
      folder = url[url.length - 2];
      public_id = url[url.length - 1];
      url = `http://localhost:8000/api/images/${pk}/${username}/${folder}/${public_id}/${img_func}/delete`;

      return fetch(url).then(res=>res.json()).then(result=>result).catch(err=>{console.log(err)})
    }
  }

  function deleteImageAsync(elem){
    let id = elem.getAttribute("id");
    id = id.split("-")[0];

      makeDeleteRequest(id).then(result=>{
        if(result["result"] === "ok"){
          let elementsToDelete = checkResponse(result,id);
          elementsToDelete.forEach(elem=>{
            removeElement(elem);
          })
        }
      })

  }


// #########################################################################

  function openUploadWidget(elem){
       let cloudName = "raymondndibe";
       let options = {};
       let isProfilePic = elem.classList.contains("profile_pic");
       let isBackgroundPic = elem.classList.contains("background_pic");
       let isPostHeaderImage = elem.classList.contains("post_header_image");
       let isCartegoryImage = elem.classList.contains("cartegory_image");


       if (isProfilePic || isBackgroundPic ){

         options = {
           uploadPreset: "profile_pictures",
           sources: ["local","url","camera","facebook","instagram"],
           multiple: false,
           cropping: true,
           showSkipCropButton: true,
           tags: isProfilePic ? ["profile_pic"] : ["background_pic"],
           resourceType: "image",
           maxFileSize: 1000000,
           form : ".user_pic_form",
           fieldName: isProfilePic ? "profile_pic_url" : "background_pic_url",
           thumbnails: isProfilePic ? ".profile_pic_thumbnails" : ".background_pic_thumbnails",
           thumbnailTransformation:[ {width: 100, height: 100, crop: 'fill'}]
         };

       } else if (isCartegoryImage) {
         options = {
           uploadPreset: "cartegory_images",
           sources: ["local","url","camera","facebook","instagram"],
           multiple: false,
           cropping: true,
           showSkipCropButton: true,
           tags: ["users", "content"],
           uploadSignature:getUploadSignatureOption,
           resourceType: "image",
           maxFileSize: 1000000,
           form : ".my_form",
           fieldName: "my_field_name",
           thumbnails: ".my_image_thumb_nail",
           thumbnailTransformation:[ {width: 200, height: 200, crop: 'fill'}, {effect: 'sepia'} ],
           buttonCaption: "Upload Profile Pic"
         };
       }


       let widget = cloudinary.createUploadWidget(options,(error, result) => {
         console.log("callback was called ooo");
       if (result && result.event === "success") {
         if (isProfilePic || isBackgroundPic){
           let img_func = isProfilePic ? "profile_pic" : "background_pic";
           let prev_thubmnail = document.querySelector(`.${img_func}_thumbnail`);
           let cloudinary_thumbnail = document.querySelectorAll(`.${img_func}_thumbnails .cloudinary-thumbnail`);
           let hidden_field = document.querySelectorAll(`.user_pic_form [name="${img_func}_url"]`);

           if(prev_thubmnail){
             makeDeleteRequest(img_func).then(result=>{
               if(result["result"] === "ok"){
                 removeElement(prev_thubmnail);
               }
             })
           }
           else if(cloudinary_thumbnail.length > 1){
             makeDeleteRequest(img_func).then(result=>{
               if(result["result"] === "ok"){
                 [cloudinary_thumbnail[0],hidden_field[0]].forEach(elem=>{
                   removeElement(elem);
                 })
               }
             })
         }

         }
       else if (elem.classList.contains("post_header_image")
           || elem.classList.contains("cartegory_image")) {
        }
      };

     });

     widget.update(options);
     widget.open();


  }
