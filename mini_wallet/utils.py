from rest_framework import status
from rest_framework.views import exception_handler

def apiSuccess(data=None, status_code=status.HTTP_200_OK):
	'''
		API success reponse formatter
	'''
	status_text = "success"
	if "error" in data:
		status_text = "fail"

	defaultsData = {}
	return {
		"status" : status_text,
		"data": (defaultsData if data is None else data)
	}

def apiError(apiexception):
	'''
		Error formatter for non ApiView errors
	'''
	print("IN erroror")
	return {
		"status_code":apiexception.status_code,
		"errors":{
			"type":apiexception.default_error_type,
			"detail":apiexception.detail
		}
	}

def custom_exception_handler(exc, context):
	# Call REST framework's default exception handler first, 
	# to get the standard error response.
	response = exception_handler(exc, context)
	# Now update response data with custom data.
	if response is not None:
		res = {
			"status": "fail",
			"error": response.data
		}
		response.data = res
	return response