	
$(function()
{
	helpdown = false;
	$("#helpDiv").hide();
	$("#helpButton").click(function()
	{
		if (helpdown)
		{
			//this.innerHTML = "Help..."
			$("#helpDiv").slideUp(1000, resize_right_bar());
			helpdown = false;
		}
		else
		{
			//this.innerHTML = "Hide..."		
			$("#helpDiv").slideDown(1000, resize_right_bar());
			helpdown = true;
		}		
		
	});
	
	
	feedbackdown = false;
	$("#feedbackDiv").hide();
	$("#feedbackButton").click(function()
	{
		if (feedbackdown)
		{
			//this.innerHTML = "Help..."
			$("#feedbackDiv").slideUp(1000, resize_right_bar());
			feedbackdown = false;
		}
		else
		{
			//this.innerHTML = "Hide..."		
			$("#feedbackDiv").slideDown(1000, resize_right_bar());
			feedbackdown = true;
		}		
		
	});	
	
});