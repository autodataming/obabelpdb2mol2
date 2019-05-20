$.ajax({ url:'/longtask?pdbfile=%s'%file.name,type:'GET',
success:function(result)
{
  console.log("result:"+file.name);

},
error:function(){console.log("error")} , 
});