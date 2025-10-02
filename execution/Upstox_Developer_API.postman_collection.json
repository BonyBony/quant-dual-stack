{
	"info": {
		"_postman_id": "628c6320-6b30-4c04-9945-7de283730c26",
		"name": "Upstox Developer API",
		"description": "Build your App on the Upstox platform\n\n<img src=\"/developer/api-documentation/images/brokerage_free_banner.png\" alt=\"Banner\">\n\n<a href=\"https://marketing-creative-and-docs.s3.ap-south-1.amazonaws.com/API_T%26C/T%26C+apply.pdf\">\\* Terms and Conditions</a>\n\n<h2>Introduction</h2>\n\nUpstox API is a set of rest APIs that provide data required to build a complete investment and trading platform. Execute orders in real time, manage user portfolio, stream live market data (using Websocket), and more, with the easy to understand API collection.\n\nAll requests are over HTTPS and the requests are sent with the content-type ‘application/json’. Developers have the option of choosing the response type as JSON or CSV for a few API calls.\n\nTo be able to use these APIs you need to create an App in the Developer Console and generate your **apiKey** and **apiSecret**. You can use a redirect URL which will be called after the login flow.\n\nIf you are a **trader**, you can directly create apps from Upstox mobile app or the desktop platform itself from **Apps** sections inside the **Account** Tab. Head over to\n\n<a href=\"http://account.upstox.com/developer/apps\">account.upstox.com/developer/apps</a>\n\n.  \n  \nIf you are a **business** looking to integrate Upstox APIs, reach out to us and we will get a custom app created for you in no time.\n\nIt is highly recommended that you do not embed the **apiSecret** in your frontend app. Create a remote backend which does the handshake on behalf of the frontend app. Marking the apiSecret in the frontend app will make your app vulnerable to threats and potential issues.",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "28774758"
	},
	"item": [
		{
			"name": "Login/OAuth",
			"item": [
				{
					"name": "Authorize API",
					"request": {
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/login/authorization/dialog?client_id=<string>&redirect_uri=<string>&state=<string>&scope=<string>",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"login",
								"authorization",
								"dialog"
							],
							"query": [
								{
									"key": "client_id",
									"value": "<string>",
									"description": "(Required) "
								},
								{
									"key": "redirect_uri",
									"value": "<string>",
									"description": "(Required) "
								},
								{
									"key": "state",
									"value": "<string>"
								},
								{
									"key": "scope",
									"value": "<string>"
								}
							]
						},
						"description": "This provides details on the login endpoint."
					},
					"response": [
						{
							"name": "Successful Operation",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/login/authorization/dialog?client_id=<string>&redirect_uri=<string>&state=<string>&scope=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"dialog"
									],
									"query": [
										{
											"key": "client_id",
											"value": "<string>"
										},
										{
											"key": "redirect_uri",
											"value": "<string>"
										},
										{
											"key": "state",
											"value": "<string>"
										},
										{
											"key": "scope",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Found",
							"code": 302,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "text/plain"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "UDAPI1018 - Redirect URI is required",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/login/authorization/dialog?client_id=<string>&redirect_uri=<string>&state=<string>&scope=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"dialog"
									],
									"query": [
										{
											"key": "client_id",
											"value": "<string>"
										},
										{
											"key": "redirect_uri",
											"value": "<string>"
										},
										{
											"key": "state",
											"value": "<string>"
										},
										{
											"key": "scope",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Untitled Response",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/login/authorization/dialog?client_id=<string>&redirect_uri=<string>&state=<string>&scope=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"dialog"
									],
									"query": [
										{
											"key": "client_id",
											"value": "<string>"
										},
										{
											"key": "redirect_uri",
											"value": "<string>"
										},
										{
											"key": "state",
											"value": "<string>"
										},
										{
											"key": "scope",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/login/authorization/dialog?client_id=<string>&redirect_uri=<string>&state=<string>&scope=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"dialog"
									],
									"query": [
										{
											"key": "client_id",
											"value": "<string>"
										},
										{
											"key": "redirect_uri",
											"value": "<string>"
										},
										{
											"key": "state",
											"value": "<string>"
										},
										{
											"key": "scope",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/login/authorization/dialog?client_id=<string>&redirect_uri=<string>&state=<string>&scope=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"dialog"
									],
									"query": [
										{
											"key": "client_id",
											"value": "<string>"
										},
										{
											"key": "redirect_uri",
											"value": "<string>"
										},
										{
											"key": "state",
											"value": "<string>"
										},
										{
											"key": "scope",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/login/authorization/dialog?client_id=<string>&redirect_uri=<string>&state=<string>&scope=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"dialog"
									],
									"query": [
										{
											"key": "client_id",
											"value": "<string>"
										},
										{
											"key": "redirect_uri",
											"value": "<string>"
										},
										{
											"key": "state",
											"value": "<string>"
										},
										{
											"key": "scope",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Get token API",
					"event": [
						{
							"listen": "test",
							"script": {
								"exec": [
									"let jsonResponse = pm.response.json();",
									"",
									"if (jsonResponse.access_token) {",
									"    pm.collectionVariables.set(\"accessToken\", jsonResponse.access_token);",
									"    console.log(\"Access token set!\");",
									"} else {",
									"    console.log(\"Access token not found in the response.\");",
									"}",
									""
								],
								"type": "text/javascript"
							}
						}
					],
					"request": {
						"method": "POST",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Content-Type",
								"value": "application/x-www-form-urlencoded"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"body": {
							"mode": "urlencoded",
							"urlencoded": [
								{
									"key": "client_id",
									"value": "6e46d831-d6d7-46b2-83f7-b9509fbde35b",
									"description": "(Required) OAuth API key that is a public identifier for app"
								},
								{
									"key": "client_secret",
									"value": "dcba5gizzp",
									"description": "(Required) OAuth client secret that is a private secret known only to app and authorization server"
								},
								{
									"key": "code",
									"value": "beTcHw",
									"description": "(Required) "
								},
								{
									"key": "grant_type",
									"value": "authorization_code",
									"description": "(Required) Type of grant used to get an access token"
								},
								{
									"key": "redirect_uri",
									"value": "https://127.0.0.1/upstox",
									"description": "(Required) Authorization server will redirect the user back to the application via redirect url"
								}
							]
						},
						"url": {
							"raw": "{{baseUrl}}/login/authorization/token",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"login",
								"authorization",
								"token"
							]
						},
						"description": "This API provides the functionality to obtain opaque token from authorization_code exchange and also provides the user’s profile in the same response."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "urlencoded",
									"urlencoded": [
										{
											"key": "client_id",
											"value": "<string>",
											"description": "(Required) OAuth API key that is a public identifier for app"
										},
										{
											"key": "client_secret",
											"value": "<string>",
											"description": "(Required) OAuth client secret that is a private secret known only to app and authorization server"
										},
										{
											"key": "code",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "grant_type",
											"value": "<string>",
											"description": "(Required) Type of grant used to get an access token"
										},
										{
											"key": "redirect_uri",
											"value": "<string>",
											"description": "(Required) Authorization server will redirect the user back to the application via redirect url"
										}
									]
								},
								"url": {
									"raw": "{{baseUrl}}/login/authorization/token",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"token"
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"email\": \"client@email.com\",\n  \"exchanges\": [\n    \"NSE\",\n    \"NSE\"\n  ],\n  \"products\": [\n    \"D\",\n    \"D\"\n  ],\n  \"broker\": \"UPSTOX\",\n  \"user_id\": \"202251\",\n  \"user_name\": \"client\",\n  \"order_types\": [\n    \"LIMIT\",\n    \"LIMIT\"\n  ],\n  \"user_type\": \"individual\",\n  \"poa\": true,\n  \"is_active\": true,\n  \"access_token\": \"quis do ut laborum\"\n}"
						},
						{
							"name": "UDAPI1017 - API Key is required <br/>UDAPI1018 - Redirect URI is required <br/>UDAPI1022 - Code is required <br/>UDAPI1023 - Grant type is required <br/>UDAPI1024 - App Secret is required <br/>",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "urlencoded",
									"urlencoded": [
										{
											"key": "client_id",
											"value": "<string>",
											"description": "(Required) OAuth API key that is a public identifier for app"
										},
										{
											"key": "client_secret",
											"value": "<string>",
											"description": "(Required) OAuth client secret that is a private secret known only to app and authorization server"
										},
										{
											"key": "code",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "grant_type",
											"value": "<string>",
											"description": "(Required) Type of grant used to get an access token"
										},
										{
											"key": "redirect_uri",
											"value": "<string>",
											"description": "(Required) Authorization server will redirect the user back to the application via redirect url"
										}
									]
								},
								"url": {
									"raw": "{{baseUrl}}/login/authorization/token",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"token"
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Untitled Response",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "urlencoded",
									"urlencoded": [
										{
											"key": "client_id",
											"value": "<string>",
											"description": "(Required) OAuth API key that is a public identifier for app"
										},
										{
											"key": "client_secret",
											"value": "<string>",
											"description": "(Required) OAuth client secret that is a private secret known only to app and authorization server"
										},
										{
											"key": "code",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "grant_type",
											"value": "<string>",
											"description": "(Required) Type of grant used to get an access token"
										},
										{
											"key": "redirect_uri",
											"value": "<string>",
											"description": "(Required) Authorization server will redirect the user back to the application via redirect url"
										}
									]
								},
								"url": {
									"raw": "{{baseUrl}}/login/authorization/token",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"token"
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "urlencoded",
									"urlencoded": [
										{
											"key": "client_id",
											"value": "<string>",
											"description": "(Required) OAuth API key that is a public identifier for app"
										},
										{
											"key": "client_secret",
											"value": "<string>",
											"description": "(Required) OAuth client secret that is a private secret known only to app and authorization server"
										},
										{
											"key": "code",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "grant_type",
											"value": "<string>",
											"description": "(Required) Type of grant used to get an access token"
										},
										{
											"key": "redirect_uri",
											"value": "<string>",
											"description": "(Required) Authorization server will redirect the user back to the application via redirect url"
										}
									]
								},
								"url": {
									"raw": "{{baseUrl}}/login/authorization/token",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"token"
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "urlencoded",
									"urlencoded": [
										{
											"key": "client_id",
											"value": "<string>",
											"description": "(Required) OAuth API key that is a public identifier for app"
										},
										{
											"key": "client_secret",
											"value": "<string>",
											"description": "(Required) OAuth client secret that is a private secret known only to app and authorization server"
										},
										{
											"key": "code",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "grant_type",
											"value": "<string>",
											"description": "(Required) Type of grant used to get an access token"
										},
										{
											"key": "redirect_uri",
											"value": "<string>",
											"description": "(Required) Authorization server will redirect the user back to the application via redirect url"
										}
									]
								},
								"url": {
									"raw": "{{baseUrl}}/login/authorization/token",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"token"
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "urlencoded",
									"urlencoded": [
										{
											"key": "client_id",
											"value": "<string>",
											"description": "(Required) OAuth API key that is a public identifier for app"
										},
										{
											"key": "client_secret",
											"value": "<string>",
											"description": "(Required) OAuth client secret that is a private secret known only to app and authorization server"
										},
										{
											"key": "code",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "grant_type",
											"value": "<string>",
											"description": "(Required) Type of grant used to get an access token"
										},
										{
											"key": "redirect_uri",
											"value": "<string>",
											"description": "(Required) Authorization server will redirect the user back to the application via redirect url"
										}
									]
								},
								"url": {
									"raw": "{{baseUrl}}/login/authorization/token",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"login",
										"authorization",
										"token"
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Logout",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "DELETE",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/logout",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"logout"
							]
						},
						"description": "Logout"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/logout",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"logout"
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": true\n}"
						},
						{
							"name": "Bad Request",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/logout",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"logout"
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Authorization Failure",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/logout",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"logout"
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"cause\": {\n    \"stackTrace\": [\n      {\n        \"classLoaderName\": \"fugiat Duis\",\n        \"moduleName\": \"qui voluptate consectetur\",\n        \"moduleVersion\": \"enim\",\n        \"methodName\": \"amet do in\",\n        \"fileName\": \"officia do\",\n        \"lineNumber\": 20513379,\n        \"className\": \"nisi ea tempor\",\n        \"nativeMethod\": false\n      },\n      {\n        \"classLoaderName\": \"cupidatat occaecat\",\n        \"moduleName\": \"aliquip occaecat fugiat\",\n        \"moduleVersion\": \"Except\",\n        \"methodName\": \"Excepteur quis\",\n        \"fileName\": \"Lorem consequat ullamco aliqua\",\n        \"lineNumber\": -66851788,\n        \"className\": \"mollit\",\n        \"nativeMethod\": false\n      }\n    ],\n    \"message\": \"consectetur deserunt ad Excepteur cupidatat\",\n    \"suppressed\": [\n      {\n        \"stackTrace\": [\n          {\n            \"classLoaderName\": \"culpa qui eiusmod\",\n            \"moduleName\": \"exercitation dolor\",\n            \"moduleVersion\": \"aute sint eu\",\n            \"methodName\": \"ips\",\n            \"fileName\": \"culpa aute ad non\",\n            \"lineNumber\": 25603045,\n            \"className\": \"nostrud consectetur in\",\n            \"nativeMethod\": true\n          },\n          {\n            \"classLoaderName\": \"dolor aute ad\",\n            \"moduleName\": \"fugiat\",\n            \"moduleVersion\": \"nisi quis Lorem sed reprehenderit\",\n            \"methodName\": \"in in aliquip\",\n            \"fileName\": \"labore\",\n            \"lineNumber\": 9733470,\n            \"className\": \"dolor non id officia\",\n            \"nativeMethod\": true\n          }\n        ],\n        \"message\": \"cupidatat magna id\",\n        \"localizedMessage\": \"irure\"\n      },\n      {\n        \"stackTrace\": [\n          {\n            \"classLoaderName\": \"minim amet\",\n            \"moduleName\": \"sunt proident\",\n            \"moduleVersion\": \"qui sed ad dolor\",\n            \"methodName\": \"i\",\n            \"fileName\": \"dolor ut\",\n            \"lineNumber\": -29738441,\n            \"className\": \"dolore\",\n            \"nativeMethod\": false\n          },\n          {\n            \"classLoaderName\": \"tempor elit\",\n            \"moduleName\": \"non esse elit veniam\",\n            \"moduleVersion\": \"ut adipisicing aute elit\",\n            \"methodName\": \"nostrud ut\",\n            \"fileName\": \"incididunt sed in aliquip\",\n            \"lineNumber\": -54027213,\n            \"className\": \"nostrud nisi qui\",\n            \"nativeMethod\": true\n          }\n        ],\n        \"message\": \"consequat esse nisi\",\n        \"localizedMessage\": \"Lorem mi\"\n      }\n    ],\n    \"localizedMessage\": \"sint velit anim\"\n  },\n  \"stackTrace\": [\n    {\n      \"classLoaderName\": \"veniam id adipisicing exercitation\",\n      \"moduleName\": \"adipisicing\",\n      \"moduleVersion\": \"voluptate Duis exercitati\",\n      \"methodName\": \"ad amet magna labore\",\n      \"fileName\": \"amet\",\n      \"lineNumber\": 70284461,\n      \"className\": \"proident commodo ipsum\",\n      \"nativeMethod\": false\n    },\n    {\n      \"classLoaderName\": \"aliquip laboris exercitation\",\n      \"moduleName\": \"laboris velit\",\n      \"moduleVersion\": \"nisi aliquip\",\n      \"methodName\": \"reprehenderit aute sed\",\n      \"fileName\": \"labor\",\n      \"lineNumber\": -88915913,\n      \"className\": \"consectetu\",\n      \"nativeMethod\": true\n    }\n  ],\n  \"message\": \"Excepteur amet aute\",\n  \"suppressed\": [\n    {\n      \"stackTrace\": [\n        {\n          \"classLoaderName\": \"sit quis dolore Excepteur dolor\",\n          \"moduleName\": \"reprehenderit quis officia\",\n          \"moduleVersion\": \"tempor dolor nisi fugiat\",\n          \"methodName\": \"quis do elit\",\n          \"fileName\": \"nulla reprehenderit occaecat commodo\",\n          \"lineNumber\": -35779043,\n          \"className\": \"adipisicing ex amet\",\n          \"nativeMethod\": true\n        },\n        {\n          \"classLoaderName\": \"ea amet\",\n          \"moduleName\": \"aliqua officia\",\n          \"moduleVersion\": \"eiusmod consequat\",\n          \"methodName\": \"sunt mollit deserunt\",\n          \"fileName\": \"ut proident commodo ea\",\n          \"lineNumber\": 39644824,\n          \"className\": \"do magna ullamco Duis irure\",\n          \"nativeMethod\": true\n        }\n      ],\n      \"message\": \"aute enim in\",\n      \"localizedMessage\": \"officia in eiusmod consectetur fugiat\"\n    },\n    {\n      \"stackTrace\": [\n        {\n          \"classLoaderName\": \"officia eiusmod fugiat mollit cupidatat\",\n          \"moduleName\": \"ut ad deserunt\",\n          \"moduleVersion\": \"laboris dolore\",\n          \"methodName\": \"et velit esse\",\n          \"fileName\": \"sed nulla in\",\n          \"lineNumber\": -25510371,\n          \"className\": \"reprehenderit in\",\n          \"nativeMethod\": true\n        },\n        {\n          \"classLoaderName\": \"consequat amet\",\n          \"moduleName\": \"Duis sunt\",\n          \"moduleVersion\": \"eiusmod dolore voluptate adipisicing\",\n          \"methodName\": \"ad quis Duis sint\",\n          \"fileName\": \"in\",\n          \"lineNumber\": 91510952,\n          \"className\": \"ex id commodo enim\",\n          \"nativeMethod\": true\n        }\n      ],\n      \"message\": \"cupidatat aliquip in in\",\n      \"localizedMessage\": \"cupidatat cillum ut et\"\n    }\n  ],\n  \"localizedMessage\": \"ad \"\n}"
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/logout",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"logout"
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/logout",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"logout"
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/logout",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"logout"
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				}
			]
		},
		{
			"name": "User",
			"item": [
				{
					"name": "Get profile",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/user/profile",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"user",
								"profile"
							]
						},
						"description": "This API allows to fetch the complete information of the user who is logged in including the products, order types and exchanges enabled for the user"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/profile",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"profile"
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": {\n    \"email\": \"client@email.com\",\n    \"exchanges\": [\n      \"NSE\",\n      \"NSE\"\n    ],\n    \"products\": [\n      \"D\",\n      \"D\"\n    ],\n    \"broker\": \"UPSTOX\",\n    \"user_id\": \"202251\",\n    \"user_name\": \"client\",\n    \"order_types\": [\n      \"LIMIT\",\n      \"LIMIT\"\n    ],\n    \"user_type\": \"individual\",\n    \"poa\": true,\n    \"is_active\": true\n  }\n}"
						},
						{
							"name": "Bad Request",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/profile",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"profile"
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/profile",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"profile"
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/profile",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"profile"
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/profile",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"profile"
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/profile",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"profile"
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Get User Fund And Margin",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/user/get-funds-and-margin?segment=SEC",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"user",
								"get-funds-and-margin"
							],
							"query": [
								{
									"key": "segment",
									"value": "SEC"
								}
							]
						},
						"description": "Shows the balance of the user in equity and commodity market."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/get-funds-and-margin?segment=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"get-funds-and-margin"
									],
									"query": [
										{
											"key": "segment",
											"value": "<string>"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": {\n    \"nisie_6\": {\n      \"used_margin\": 120.01,\n      \"payin_amount\": 0,\n      \"span_margin\": 0,\n      \"adhoc_margin\": 0,\n      \"notional_cash\": 0,\n      \"available_margin\": 200,\n      \"exposure_margin\": 0\n    },\n    \"dolor5d\": {\n      \"used_margin\": 120.01,\n      \"payin_amount\": 0,\n      \"span_margin\": 0,\n      \"adhoc_margin\": 0,\n      \"notional_cash\": 0,\n      \"available_margin\": 200,\n      \"exposure_margin\": 0\n    },\n    \"in_9\": {\n      \"used_margin\": 120.01,\n      \"payin_amount\": 0,\n      \"span_margin\": 0,\n      \"adhoc_margin\": 0,\n      \"notional_cash\": 0,\n      \"available_margin\": 200,\n      \"exposure_margin\": 0\n    }\n  }\n}"
						},
						{
							"name": "UDAPI1019 - segment is invalid",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/get-funds-and-margin?segment=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"get-funds-and-margin"
									],
									"query": [
										{
											"key": "segment",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/get-funds-and-margin?segment=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"get-funds-and-margin"
									],
									"query": [
										{
											"key": "segment",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/get-funds-and-margin?segment=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"get-funds-and-margin"
									],
									"query": [
										{
											"key": "segment",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/get-funds-and-margin?segment=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"get-funds-and-margin"
									],
									"query": [
										{
											"key": "segment",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/user/get-funds-and-margin?segment=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"user",
										"get-funds-and-margin"
									],
									"query": [
										{
											"key": "segment",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				}
			]
		},
		{
			"name": "Portfolio",
			"item": [
				{
					"name": "Convert Positions",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "PUT",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Content-Type",
								"value": "application/json"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n  \"instrument_token\": \"<string>\",\n  \"new_product\": \"<string>\",\n  \"old_product\": \"<string>\",\n  \"quantity\": \"<integer>\",\n  \"transaction_type\": \"<string>\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{baseUrl}}/portfolio/convert-position",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"portfolio",
								"convert-position"
							]
						},
						"description": "Convert the margin product of an open position"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"instrument_token\": \"151064324\",\n  \"new_product\": \"D\",\n  \"old_product\": \"I\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/portfolio/convert-position",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"convert-position"
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"data\": {\n    \"status\": \"complete\"\n  }\n}"
						},
						{
							"name": "Bad Request",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"instrument_token\": \"151064324\",\n  \"new_product\": \"D\",\n  \"old_product\": \"I\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/portfolio/convert-position",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"convert-position"
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Authorization Failure",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"instrument_token\": \"151064324\",\n  \"new_product\": \"D\",\n  \"old_product\": \"I\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/portfolio/convert-position",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"convert-position"
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"instrument_token\": \"151064324\",\n  \"new_product\": \"D\",\n  \"old_product\": \"I\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/portfolio/convert-position",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"convert-position"
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"instrument_token\": \"151064324\",\n  \"new_product\": \"D\",\n  \"old_product\": \"I\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/portfolio/convert-position",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"convert-position"
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"instrument_token\": \"151064324\",\n  \"new_product\": \"D\",\n  \"old_product\": \"I\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/portfolio/convert-position",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"convert-position"
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Get Positions",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/portfolio/short-term-positions",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"portfolio",
								"short-term-positions"
							]
						},
						"description": "Fetches the current positions for the user for the current day."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/short-term-positions",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"short-term-positions"
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"data\": [\n    {\n      \"exchange\": \"NSE\",\n      \"multiplier\": 1,\n      \"value\": 120,\n      \"pnl\": 121.01,\n      \"product\": \"D\",\n      \"instrument_token\": \"151064324\",\n      \"average_price\": 120.01,\n      \"buy_value\": 120,\n      \"overnight_quantity\": 1,\n      \"day_buy_value\": 120.01,\n      \"day_buy_price\": 120.01,\n      \"overnight_buy_amount\": 12,\n      \"overnight_buy_quantity\": 12,\n      \"day_buy_quantity\": 1,\n      \"day_sell_value\": 0,\n      \"day_sell_price\": 0,\n      \"overnight_sell_amount\": 120.01,\n      \"overnight_sell_quantity\": 0,\n      \"day_sell_quantity\": 0,\n      \"quantity\": 2,\n      \"last_price\": 120.01,\n      \"unrealised\": 121.01,\n      \"realised\": 0,\n      \"sell_value\": 0,\n      \"tradingsymbol\": \"GMR\",\n      \"close_price\": 102,\n      \"buy_price\": 102,\n      \"sell_price\": 102\n    },\n    {\n      \"exchange\": \"NSE\",\n      \"multiplier\": 1,\n      \"value\": 120,\n      \"pnl\": 121.01,\n      \"product\": \"D\",\n      \"instrument_token\": \"151064324\",\n      \"average_price\": 120.01,\n      \"buy_value\": 120,\n      \"overnight_quantity\": 1,\n      \"day_buy_value\": 120.01,\n      \"day_buy_price\": 120.01,\n      \"overnight_buy_amount\": 12,\n      \"overnight_buy_quantity\": 12,\n      \"day_buy_quantity\": 1,\n      \"day_sell_value\": 0,\n      \"day_sell_price\": 0,\n      \"overnight_sell_amount\": 120.01,\n      \"overnight_sell_quantity\": 0,\n      \"day_sell_quantity\": 0,\n      \"quantity\": 2,\n      \"last_price\": 120.01,\n      \"unrealised\": 121.01,\n      \"realised\": 0,\n      \"sell_value\": 0,\n      \"tradingsymbol\": \"GMR\",\n      \"close_price\": 102,\n      \"buy_price\": 102,\n      \"sell_price\": 102\n    }\n  ]\n}"
						},
						{
							"name": "Bad Request",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/short-term-positions",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"short-term-positions"
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Authorization Failure",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/short-term-positions",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"short-term-positions"
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/short-term-positions",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"short-term-positions"
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/short-term-positions",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"short-term-positions"
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/short-term-positions",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"short-term-positions"
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Get Holdings",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/portfolio/long-term-holdings",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"portfolio",
								"long-term-holdings"
							]
						},
						"description": "Fetches the holdings which the user has bought/sold in previous trading sessions."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/long-term-holdings",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"long-term-holdings"
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": [\n    {\n      \"isin\": \"INE118H01025\",\n      \"cnc_used_quantity\": 0,\n      \"collateral_type\": \"WC\",\n      \"company_name\": \"BSE LIM\",\n      \"haircut\": 0.23,\n      \"product\": \"D\",\n      \"quantity\": 1,\n      \"tradingsymbol\": \"BSE\",\n      \"last_price\": 120.01,\n      \"close_price\": 120.01,\n      \"pnl\": 120.01,\n      \"day_change\": 0,\n      \"day_change_percentage\": 0,\n      \"instrument_token\": \"151064324\",\n      \"average_price\": 120.01,\n      \"collateral_quantity\": 0,\n      \"collateral_update_quantity\": 0,\n      \"t1_quantity\": 0,\n      \"exchange\": \"NSE\"\n    },\n    {\n      \"isin\": \"INE118H01025\",\n      \"cnc_used_quantity\": 0,\n      \"collateral_type\": \"WC\",\n      \"company_name\": \"BSE LIM\",\n      \"haircut\": 0.23,\n      \"product\": \"D\",\n      \"quantity\": 1,\n      \"tradingsymbol\": \"BSE\",\n      \"last_price\": 120.01,\n      \"close_price\": 120.01,\n      \"pnl\": 120.01,\n      \"day_change\": 0,\n      \"day_change_percentage\": 0,\n      \"instrument_token\": \"151064324\",\n      \"average_price\": 120.01,\n      \"collateral_quantity\": 0,\n      \"collateral_update_quantity\": 0,\n      \"t1_quantity\": 0,\n      \"exchange\": \"NSE\"\n    }\n  ]\n}"
						},
						{
							"name": "Bad Request",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/long-term-holdings",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"long-term-holdings"
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Authorization Failure",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/long-term-holdings",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"long-term-holdings"
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/long-term-holdings",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"long-term-holdings"
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/long-term-holdings",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"long-term-holdings"
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/portfolio/long-term-holdings",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"portfolio",
										"long-term-holdings"
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				}
			]
		},
		{
			"name": "Order",
			"item": [
				{
					"name": "trades",
					"item": [
						{
							"name": "Get trades for order",
							"request": {
								"auth": {
									"type": "bearer",
									"bearer": [
										{
											"key": "token",
											"value": "{{accessToken}}",
											"type": "string"
										}
									]
								},
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "{{version}}"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/trades?order_id=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"trades"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>",
											"description": "(Required) The order ID for which the order to get order trades"
										}
									]
								},
								"description": "Retrieve the trades executed for an order"
							},
							"response": [
								{
									"name": "Successful",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades?order_id=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades"
											],
											"query": [
												{
													"key": "order_id",
													"value": "<string>"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"status\": \"error\",\n  \"data\": [\n    {\n      \"exchange\": \"NSE\",\n      \"product\": \"D\",\n      \"tradingsymbol\": \"GMRINFRA-EQ\",\n      \"instrument_token\": \"151064324\",\n      \"order_type\": \"MARKET\",\n      \"transaction_type\": \"BUY\",\n      \"quantity\": 1,\n      \"exchange_order_id\": \"221013001021540\",\n      \"order_id\": \"221013001021539\",\n      \"exchange_timestamp\": \"03-Aug-2017 15:03:42\",\n      \"average_price\": 299.4,\n      \"trade_id\": \"50091502\",\n      \"order_ref_id\": \"udapi-aqwsed14356\",\n      \"order_timestamp\": \"23-Apr-2021 14:22:06\"\n    },\n    {\n      \"exchange\": \"NSE\",\n      \"product\": \"D\",\n      \"tradingsymbol\": \"GMRINFRA-EQ\",\n      \"instrument_token\": \"151064324\",\n      \"order_type\": \"MARKET\",\n      \"transaction_type\": \"BUY\",\n      \"quantity\": 1,\n      \"exchange_order_id\": \"221013001021540\",\n      \"order_id\": \"221013001021539\",\n      \"exchange_timestamp\": \"03-Aug-2017 15:03:42\",\n      \"average_price\": 299.4,\n      \"trade_id\": \"50091502\",\n      \"order_ref_id\": \"udapi-aqwsed14356\",\n      \"order_timestamp\": \"23-Apr-2021 14:22:06\"\n    }\n  ]\n}"
								},
								{
									"name": "UDAPI1010 - Order id accepts only alphanumeric characters and '-'.<br>UDAPI1023 - Order id is required<br>UDAPI100010 - Unknown order id | order request rejected",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades?order_id=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades"
											],
											"query": [
												{
													"key": "order_id",
													"value": "<string>"
												}
											]
										}
									},
									"status": "Bad Request",
									"code": 400,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
								},
								{
									"name": "Unauthorized",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades?order_id=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades"
											],
											"query": [
												{
													"key": "order_id",
													"value": "<string>"
												}
											]
										}
									},
									"status": "Unauthorized",
									"code": 401,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Method Not Allowed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades?order_id=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades"
											],
											"query": [
												{
													"key": "order_id",
													"value": "<string>"
												}
											]
										}
									},
									"status": "Method Not Allowed",
									"code": 405,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Too Many Requests",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades?order_id=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades"
											],
											"query": [
												{
													"key": "order_id",
													"value": "<string>"
												}
											]
										}
									},
									"status": "Too Many Requests",
									"code": 429,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Internal Server Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades?order_id=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades"
											],
											"query": [
												{
													"key": "order_id",
													"value": "<string>"
												}
											]
										}
									},
									"status": "Internal Server Error",
									"code": 500,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								}
							]
						},
						{
							"name": "Get trades",
							"request": {
								"auth": {
									"type": "bearer",
									"bearer": [
										{
											"key": "token",
											"value": "{{accessToken}}",
											"type": "string"
										}
									]
								},
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "{{version}}"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/trades/get-trades-for-day",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"trades",
										"get-trades-for-day"
									]
								},
								"description": "Retrieve the trades executed for the day"
							},
							"response": [
								{
									"name": "Successful",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades/get-trades-for-day",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades",
												"get-trades-for-day"
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"status\": \"success\",\n  \"data\": [\n    {\n      \"exchange\": \"NSE\",\n      \"product\": \"D\",\n      \"tradingsymbol\": \"GMRINFRA-EQ\",\n      \"instrument_token\": \"151064324\",\n      \"order_type\": \"MARKET\",\n      \"transaction_type\": \"BUY\",\n      \"quantity\": 1,\n      \"exchange_order_id\": \"221013001021540\",\n      \"order_id\": \"221013001021539\",\n      \"exchange_timestamp\": \"03-Aug-2017 15:03:42\",\n      \"average_price\": 299.4,\n      \"trade_id\": \"50091502\",\n      \"order_ref_id\": \"udapi-aqwsed14356\",\n      \"order_timestamp\": \"23-Apr-2021 14:22:06\"\n    },\n    {\n      \"exchange\": \"NSE\",\n      \"product\": \"D\",\n      \"tradingsymbol\": \"GMRINFRA-EQ\",\n      \"instrument_token\": \"151064324\",\n      \"order_type\": \"MARKET\",\n      \"transaction_type\": \"BUY\",\n      \"quantity\": 1,\n      \"exchange_order_id\": \"221013001021540\",\n      \"order_id\": \"221013001021539\",\n      \"exchange_timestamp\": \"03-Aug-2017 15:03:42\",\n      \"average_price\": 299.4,\n      \"trade_id\": \"50091502\",\n      \"order_ref_id\": \"udapi-aqwsed14356\",\n      \"order_timestamp\": \"23-Apr-2021 14:22:06\"\n    }\n  ]\n}"
								},
								{
									"name": "Bad Request",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades/get-trades-for-day",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades",
												"get-trades-for-day"
											]
										}
									},
									"status": "Bad Request",
									"code": 400,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Unauthorized",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades/get-trades-for-day",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades",
												"get-trades-for-day"
											]
										}
									},
									"status": "Unauthorized",
									"code": 401,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Method Not Allowed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades/get-trades-for-day",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades",
												"get-trades-for-day"
											]
										}
									},
									"status": "Method Not Allowed",
									"code": 405,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Too Many Requests",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades/get-trades-for-day",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades",
												"get-trades-for-day"
											]
										}
									},
									"status": "Too Many Requests",
									"code": 429,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Internal Server Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/order/trades/get-trades-for-day",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"order",
												"trades",
												"get-trades-for-day"
											]
										}
									},
									"status": "Internal Server Error",
									"code": 500,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								}
							]
						}
					]
				},
				{
					"name": "Modify order",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "PUT",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Content-Type",
								"value": "application/json"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n  \"order_id\": \"<string>\",\n  \"order_type\": \"<string>\",\n  \"price\": \"<float>\",\n  \"trigger_price\": \"<float>\",\n  \"validity\": \"<string>\",\n  \"quantity\": \"<integer>\",\n  \"disclosed_quantity\": \"<integer>\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{baseUrl}}/order/modify",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"order",
								"modify"
							]
						},
						"description": "This API allows you to modify an order. For modification orderId is mandatory. With orderId you need to send the optional parameter which needs to be modified. In case the optional parameters aren't sent, the default will be considered from the original order"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"order_id\": \"1644490272000\",\n  \"order_type\": \"MARKET\",\n  \"price\": 120.01,\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"quantity\": 1,\n  \"disclosed_quantity\": 0\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/modify",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"modify"
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"data\": {\n    \"order_id\": \"1644490272000\"\n  }\n}"
						},
						{
							"name": "UDAPI100010 - Unknown order id | order request rejected",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"order_id\": \"1644490272000\",\n  \"order_type\": \"MARKET\",\n  \"price\": 120.01,\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"quantity\": 1,\n  \"disclosed_quantity\": 0\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/modify",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"modify"
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"order_id\": \"1644490272000\",\n  \"order_type\": \"MARKET\",\n  \"price\": 120.01,\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"quantity\": 1,\n  \"disclosed_quantity\": 0\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/modify",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"modify"
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"order_id\": \"1644490272000\",\n  \"order_type\": \"MARKET\",\n  \"price\": 120.01,\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"quantity\": 1,\n  \"disclosed_quantity\": 0\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/modify",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"modify"
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"order_id\": \"1644490272000\",\n  \"order_type\": \"MARKET\",\n  \"price\": 120.01,\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"quantity\": 1,\n  \"disclosed_quantity\": 0\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/modify",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"modify"
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "PUT",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"order_id\": \"1644490272000\",\n  \"order_type\": \"MARKET\",\n  \"price\": 120.01,\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"quantity\": 1,\n  \"disclosed_quantity\": 0\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/modify",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"modify"
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Place order",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "POST",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Content-Type",
								"value": "application/json"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"quantity\": 1,\n    \"product\": \"D\",\n    \"validity\": \"DAY\",\n    \"price\": 0,\n    \"tag\": \"string\",\n    \"instrument_token\": \"NSE_EQ|INE848E01016\",\n    \"order_type\": \"MARKET\",\n    \"transaction_type\": \"BUY\",\n    \"disclosed_quantity\": 0,\n    \"trigger_price\": 0,\n    \"is_amo\": false\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "{{baseUrl}}/order/place",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"order",
								"place"
							]
						},
						"description": "This API allows you to place an order to the exchange via Upstox."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"disclosed_quantity\": 0,\n  \"instrument_token\": \"NSE_EQ|INE848E01016\",\n  \"is_amo\": false,\n  \"order_type\": \"MARKET\",\n  \"price\": 0,\n  \"product\": \"D\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\",\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"tag\": \"<string>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/place",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"place"
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": {\n    \"order_id\": \"1644490272000\"\n  }\n}"
						},
						{
							"name": "Bad Request",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"disclosed_quantity\": 0,\n  \"instrument_token\": \"NSE_EQ|INE848E01016\",\n  \"is_amo\": false,\n  \"order_type\": \"MARKET\",\n  \"price\": 0,\n  \"product\": \"D\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\",\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"tag\": \"<string>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/place",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"place"
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"disclosed_quantity\": 0,\n  \"instrument_token\": \"NSE_EQ|INE848E01016\",\n  \"is_amo\": false,\n  \"order_type\": \"MARKET\",\n  \"price\": 0,\n  \"product\": \"D\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\",\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"tag\": \"<string>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/place",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"place"
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"disclosed_quantity\": 0,\n  \"instrument_token\": \"NSE_EQ|INE848E01016\",\n  \"is_amo\": false,\n  \"order_type\": \"MARKET\",\n  \"price\": 0,\n  \"product\": \"D\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\",\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"tag\": \"<string>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/place",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"place"
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"disclosed_quantity\": 0,\n  \"instrument_token\": \"NSE_EQ|INE848E01016\",\n  \"is_amo\": false,\n  \"order_type\": \"MARKET\",\n  \"price\": 0,\n  \"product\": \"D\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\",\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"tag\": \"<string>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/place",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"place"
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "POST",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"disclosed_quantity\": 0,\n  \"instrument_token\": \"NSE_EQ|INE848E01016\",\n  \"is_amo\": false,\n  \"order_type\": \"MARKET\",\n  \"price\": 0,\n  \"product\": \"D\",\n  \"quantity\": 1,\n  \"transaction_type\": \"BUY\",\n  \"trigger_price\": 0,\n  \"validity\": \"DAY\",\n  \"tag\": \"<string>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/order/place",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"place"
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Get order book",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/order/retrieve-all",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"order",
								"retrieve-all"
							]
						},
						"description": "This API provides the list of orders placed by the user. The orders placed by the user is transient for a day and is cleared by the end of the trading session. This API returns all states of the orders, namely, open, pending, and filled ones."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/retrieve-all",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"retrieve-all"
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": [\n    {\n      \"exchange\": \"NSE\",\n      \"product\": \"D\",\n      \"price\": 120.01,\n      \"quantity\": 1,\n      \"status\": \"Complete\",\n      \"guid\": \"officia commodo\",\n      \"tag\": \"elit fugiat ea Ut\",\n      \"instrument_token\": \"151064324\",\n      \"placed_by\": \"200123\",\n      \"tradingsymbol\": \"GMR\",\n      \"order_type\": \"MARKET\",\n      \"validity\": \"DAY\",\n      \"trigger_price\": 120,\n      \"disclosed_quantity\": 1,\n      \"transaction_type\": \"BUY\",\n      \"average_price\": 120.01,\n      \"filled_quantity\": -65781389,\n      \"pending_quantity\": 1,\n      \"status_message\": \"ea in ut sed\",\n      \"status_message_raw\": \"Duis esse aliqua\",\n      \"exchange_order_id\": \"221013001021540\",\n      \"parent_order_id\": \"221013001021541\",\n      \"order_id\": \"221013001021541\",\n      \"variety\": \"SIMPLE\",\n      \"order_timestamp\": \"23-Apr-2021 14:22:06\",\n      \"exchange_timestamp\": \"24-Apr-2021 14:22:06\",\n      \"is_amo\": false,\n      \"order_request_id\": \"221013001021542\",\n      \"order_ref_id\": \"udapi-12345abcd\"\n    },\n    {\n      \"exchange\": \"NSE\",\n      \"product\": \"D\",\n      \"price\": 120.01,\n      \"quantity\": 1,\n      \"status\": \"Complete\",\n      \"guid\": \"do culpa elit\",\n      \"tag\": \"nulla ex\",\n      \"instrument_token\": \"151064324\",\n      \"placed_by\": \"200123\",\n      \"tradingsymbol\": \"GMR\",\n      \"order_type\": \"MARKET\",\n      \"validity\": \"DAY\",\n      \"trigger_price\": 120,\n      \"disclosed_quantity\": 1,\n      \"transaction_type\": \"BUY\",\n      \"average_price\": 120.01,\n      \"filled_quantity\": -96502354,\n      \"pending_quantity\": 1,\n      \"status_message\": \"qui labore fugiat consequat deserunt\",\n      \"status_message_raw\": \"amet \",\n      \"exchange_order_id\": \"221013001021540\",\n      \"parent_order_id\": \"221013001021541\",\n      \"order_id\": \"221013001021541\",\n      \"variety\": \"SIMPLE\",\n      \"order_timestamp\": \"23-Apr-2021 14:22:06\",\n      \"exchange_timestamp\": \"24-Apr-2021 14:22:06\",\n      \"is_amo\": false,\n      \"order_request_id\": \"221013001021542\",\n      \"order_ref_id\": \"udapi-12345abcd\"\n    }\n  ]\n}"
						},
						{
							"name": "Bad Request",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/retrieve-all",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"retrieve-all"
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/retrieve-all",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"retrieve-all"
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/retrieve-all",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"retrieve-all"
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/retrieve-all",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"retrieve-all"
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/retrieve-all",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"retrieve-all"
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Get order history",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/order/history?order_id=230929010212328",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"order",
								"history"
							],
							"query": [
								{
									"key": "order_id",
									"value": "230929010212328",
									"description": "The order reference ID for which the order history is required"
								},
								{
									"key": "tag",
									"value": "<string>",
									"description": "The unique tag of the order for which the order history is being requested",
									"disabled": true
								}
							]
						},
						"description": "This API provides the details of the particular order the user has placed. The orders placed by the user is transient for a day and are cleared by the end of the trading session. This API returns all states of the orders, namely, open, pending, and filled ones.\n\nThe order history can be requested either using order_id or tag.\n\nIf both the options are passed, the history of the order which precisely matches both the order_id and tag will be returned in the response.\n\nIf only the tag is passed, the history of all the associated orders which matches the tag will be shared in the response."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/history?order_id=<string>&tag=2qdqjppebx",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"history"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										},
										{
											"key": "tag",
											"value": "2qdqjppebx"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"data\": [\n    {\n      \"exchange\": \"NSE\",\n      \"price\": 120.01,\n      \"product\": \"D\",\n      \"quantity\": 1,\n      \"status\": \"complete\",\n      \"tag\": \"anim non voluptate ut\",\n      \"validity\": \"DAY\",\n      \"average_price\": 120.01,\n      \"disclosed_quantity\": 1,\n      \"exchange_order_id\": \"221013001021540\",\n      \"exchange_timestamp\": \"03-Aug-2017 15:03:42\",\n      \"instrument_token\": \"151064324\",\n      \"is_amo\": false,\n      \"status_message\": \"magna exercitation eiusmod consequat adipisicing\",\n      \"order_id\": \"221013001021541\",\n      \"order_request_id\": \"221013001021542\",\n      \"order_type\": \"MARKET\",\n      \"parent_order_id\": \"221013001021543\",\n      \"tradingsymbol\": \"GMR\",\n      \"order_timestamp\": \"23-Apr-2021 14:22:06\",\n      \"filled_quantity\": 1,\n      \"transaction_type\": \"BUY\",\n      \"trigger_price\": 120.01,\n      \"placed_by\": \"200123\",\n      \"variety\": \"SIMPLE\"\n    },\n    {\n      \"exchange\": \"NSE\",\n      \"price\": 120.01,\n      \"product\": \"D\",\n      \"quantity\": 1,\n      \"status\": \"complete\",\n      \"tag\": \"aliqua amet deserunt esse\",\n      \"validity\": \"DAY\",\n      \"average_price\": 120.01,\n      \"disclosed_quantity\": 1,\n      \"exchange_order_id\": \"221013001021540\",\n      \"exchange_timestamp\": \"03-Aug-2017 15:03:42\",\n      \"instrument_token\": \"151064324\",\n      \"is_amo\": false,\n      \"status_message\": \"sit consectetur\",\n      \"order_id\": \"221013001021541\",\n      \"order_request_id\": \"221013001021542\",\n      \"order_type\": \"MARKET\",\n      \"parent_order_id\": \"221013001021543\",\n      \"tradingsymbol\": \"GMR\",\n      \"order_timestamp\": \"23-Apr-2021 14:22:06\",\n      \"filled_quantity\": 1,\n      \"transaction_type\": \"BUY\",\n      \"trigger_price\": 120.01,\n      \"placed_by\": \"200123\",\n      \"variety\": \"SIMPLE\"\n    }\n  ]\n}"
						},
						{
							"name": "UDAPI1010 - Order id accepts only alphanumeric characters and '-'<br>UDAPI1023 - Order id is required<br>UDAPI100010 - Unknown order id | order request rejected",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/history?order_id=<string>&tag=2qdqjppebx",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"history"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										},
										{
											"key": "tag",
											"value": "2qdqjppebx"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/history?order_id=<string>&tag=2qdqjppebx",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"history"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										},
										{
											"key": "tag",
											"value": "2qdqjppebx"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/history?order_id=<string>&tag=2qdqjppebx",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"history"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										},
										{
											"key": "tag",
											"value": "2qdqjppebx"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/history?order_id=<string>&tag=2qdqjppebx",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"history"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										},
										{
											"key": "tag",
											"value": "2qdqjppebx"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/history?order_id=<string>&tag=2qdqjppebx",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"history"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										},
										{
											"key": "tag",
											"value": "2qdqjppebx"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Cancel order",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "DELETE",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/order/cancel?order_id=<string>",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"order",
								"cancel"
							],
							"query": [
								{
									"key": "order_id",
									"value": "<string>",
									"description": "(Required) The order ID for which the order must be cancelled"
								}
							]
						},
						"description": "Cancel order API can be used for two purposes:\nCancelling an open order which could be an AMO or a normal order\nIt is also used to EXIT a CO or OCO(bracket order)"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/cancel?order_id=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"cancel"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"data\": {\n    \"order_id\": \"1644490272000\"\n  }\n}"
						},
						{
							"name": "UDAPI1010 - Order id accepts only alphanumeric characters and '-'.<br>UDAPI1023 - Order id is required<br>UDAPI100010 - Unknown order id | order request rejected",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/cancel?order_id=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"cancel"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/cancel?order_id=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"cancel"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/cancel?order_id=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"cancel"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/cancel?order_id=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"cancel"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "DELETE",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/order/cancel?order_id=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"order",
										"cancel"
									],
									"query": [
										{
											"key": "order_id",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				}
			]
		},
		{
			"name": "Market Quote",
			"item": [
				{
					"name": "Market quotes and instruments - Full market quotes",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/market-quote/quotes?symbol=NSE_EQ|INE848E01016",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"market-quote",
								"quotes"
							],
							"query": [
								{
									"key": "symbol",
									"value": "NSE_EQ|INE848E01016",
									"description": "(Required) Comma separated list of symbols"
								}
							]
						},
						"description": "This API provides the functionality to retrieve the full market quotes for one or more instruments.This API returns the complete market data snapshot of up to 500 instruments in one go."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/quotes?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"quotes"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": {\n    \"exercitation_34e\": {\n      \"ohlc\": {\n        \"open\": 120.01,\n        \"high\": 121,\n        \"low\": 119,\n        \"close\": 120\n      },\n      \"depth\": {\n        \"buy\": [\n          {\n            \"quantity\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            },\n            \"price\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            },\n            \"orders\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            }\n          },\n          {\n            \"quantity\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            },\n            \"price\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            },\n            \"orders\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            }\n          }\n        ],\n        \"sell\": [\n          {\n            \"quantity\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            },\n            \"price\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            },\n            \"orders\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            }\n          },\n          {\n            \"quantity\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            },\n            \"price\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            },\n            \"orders\": {\n              \"value\": \"<Error: Too many levels of nesting to fake this schema>\"\n            }\n          }\n        ]\n      },\n      \"timestamp\": \"Duis deserunt\",\n      \"instrument_token\": \"NSE_EQ|INE160A01022\",\n      \"symbol\": \"NHPC\",\n      \"last_price\": 120.01,\n      \"volume\": 2344451,\n      \"average_price\": 120.01,\n      \"oi\": 0,\n      \"net_change\": 0.01,\n      \"total_buy_quantity\": 0,\n      \"total_sell_quantity\": 0,\n      \"lower_circuit_limit\": 119,\n      \"upper_circuit_limit\": 121,\n      \"last_trade_time\": \"esse Excepteur dolore\",\n      \"oi_day_high\": 0,\n      \"oi_day_low\": 0\n    }\n  }\n}"
						},
						{
							"name": "UDAPI1009 - symbol is required<br>UDAPI1011 - symbol is of invalid format<br>UDAPI100011 - Invalid Instrument key",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/quotes?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"quotes"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/quotes?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"quotes"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/quotes?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"quotes"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/quotes?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"quotes"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/quotes?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"quotes"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Market quotes and instruments - OHLC quotes",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/market-quote/ohlc?symbol=NSE_EQ|INE848E01016&interval=1d",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"market-quote",
								"ohlc"
							],
							"query": [
								{
									"key": "symbol",
									"value": "NSE_EQ|INE848E01016",
									"description": "(Required) Comma separated list of symbols"
								},
								{
									"key": "interval",
									"value": "1d",
									"description": "(Required) Interval to get ohlc data"
								}
							]
						},
						"description": "This API provides the functionality to retrieve the OHLC quotes for one or more instruments.This API returns the OHLC snapshots of up to 1000 instruments in one go."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ohlc?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039&interval=1d",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ohlc"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										},
										{
											"key": "interval",
											"value": "1d"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": {\n    \"in_b01\": {\n      \"ohlc\": {\n        \"open\": 120.01,\n        \"high\": 121,\n        \"low\": 119,\n        \"close\": 120\n      },\n      \"last_price\": 120.01,\n      \"instrument_token\": \"minim ad\"\n    },\n    \"ea631\": {\n      \"ohlc\": {\n        \"open\": 120.01,\n        \"high\": 121,\n        \"low\": 119,\n        \"close\": 120\n      },\n      \"last_price\": 120.01,\n      \"instrument_token\": \"non in ex culpa aliqua\"\n    },\n    \"elit6\": {\n      \"ohlc\": {\n        \"open\": 120.01,\n        \"high\": 121,\n        \"low\": 119,\n        \"close\": 120\n      },\n      \"last_price\": 120.01,\n      \"instrument_token\": \"esse cillum\"\n    },\n    \"sint1f9\": {\n      \"ohlc\": {\n        \"open\": 120.01,\n        \"high\": 121,\n        \"low\": 119,\n        \"close\": 120\n      },\n      \"last_price\": 120.01,\n      \"instrument_token\": \"aute ex non in\"\n    }\n  }\n}"
						},
						{
							"name": "UDAPI1009 - symbol is required<br>UDAPI1011 - symbol is of invalid format<br>UDAPI1027 - interval is required<br>UDAPI1028 - Invalid interval<br>UDAPI100011 - Invalid Instrument key",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ohlc?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039&interval=1d",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ohlc"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										},
										{
											"key": "interval",
											"value": "1d"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ohlc?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039&interval=1d",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ohlc"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										},
										{
											"key": "interval",
											"value": "1d"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ohlc?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039&interval=1d",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ohlc"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										},
										{
											"key": "interval",
											"value": "1d"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ohlc?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039&interval=1d",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ohlc"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										},
										{
											"key": "interval",
											"value": "1d"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ohlc?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039&interval=1d",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ohlc"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										},
										{
											"key": "interval",
											"value": "1d"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Market quotes and instruments - LTP quotes.",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/market-quote/ltp?symbol=NSE_EQ|INE848E01016",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"market-quote",
								"ltp"
							],
							"query": [
								{
									"key": "symbol",
									"value": "NSE_EQ|INE848E01016",
									"description": "(Required) Comma separated list of symbols"
								}
							]
						},
						"description": "This API provides the functionality to retrieve the LTP quotes for one or more instruments.This API returns the LTPs of up to 1000 instruments in one go."
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ltp?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ltp"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"data\": {\n    \"laborum9\": {\n      \"last_price\": 120.01,\n      \"instrument_token\": \"dolor velit cillum Excepteur\"\n    },\n    \"commodo_1\": {\n      \"last_price\": 120.01,\n      \"instrument_token\": \"exercitation adipisicing dolore\"\n    },\n    \"sit68\": {\n      \"last_price\": 120.01,\n      \"instrument_token\": \"et eu\"\n    }\n  }\n}"
						},
						{
							"name": "UDAPI1009 - symbol is required<br>UDAPI1011 - symbol is of invalid format<br>UDAPI100011 - Invalid Instrument key",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ltp?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ltp"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ltp?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ltp"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ltp?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ltp"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ltp?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ltp"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/market-quote/ltp?symbol=NSE_EQ|INE848E01016,NSE_EQ|INE848E01039",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"market-quote",
										"ltp"
									],
									"query": [
										{
											"key": "symbol",
											"value": "NSE_EQ|INE848E01016,NSE_EQ|INE848E01039"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				}
			]
		},
		{
			"name": "Trade Profit And Loss",
			"item": [
				{
					"name": "Get profit and loss meta data on trades",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/trade/profit-loss/metadata?from_date=<string>&to_date=<string>&segment=<string>&financial_year=<string>",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"trade",
								"profit-loss",
								"metadata"
							],
							"query": [
								{
									"key": "from_date",
									"value": "<string>",
									"description": "Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format"
								},
								{
									"key": "to_date",
									"value": "<string>",
									"description": "Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format"
								},
								{
									"key": "segment",
									"value": "<string>",
									"description": "(Required) Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives"
								},
								{
									"key": "financial_year",
									"value": "<string>",
									"description": "(Required) Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122"
								}
							]
						},
						"description": "This API gives the data of the realised Profit and Loss report requested by a user"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/metadata?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"metadata"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"data\": {\n    \"trades_count\": 10,\n    \"page_size_limit\": 5000\n  }\n}"
						},
						{
							"name": "UDAPI1070 - The financial_year is required<br>UDAPI1067 - The ''segment'' is required<br>UDAPI1066 - The ''segment'' is invalid<br>UDAPI1073 - Financial year should have max length of 4<br>UDAPI1068 - The start_date is required<br>UDAPI1069 - The end_date",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/metadata?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"metadata"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/metadata?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"metadata"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/metadata?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"metadata"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/metadata?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"metadata"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/metadata?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"metadata"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Get Trade-wise Profit and Loss Report Data",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/trade/profit-loss/data?from_date=<string>&to_date=<string>&segment=<string>&financial_year=<string>&page_number=<integer>&page_size=<integer>",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"trade",
								"profit-loss",
								"data"
							],
							"query": [
								{
									"key": "from_date",
									"value": "<string>",
									"description": "Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format"
								},
								{
									"key": "to_date",
									"value": "<string>",
									"description": "Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format"
								},
								{
									"key": "segment",
									"value": "<string>",
									"description": "(Required) Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives"
								},
								{
									"key": "financial_year",
									"value": "<string>",
									"description": "(Required) Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122"
								},
								{
									"key": "page_number",
									"value": "<integer>",
									"description": "(Required) Page Number, the pages are starting from 1"
								},
								{
									"key": "page_size",
									"value": "<integer>",
									"description": "(Required) Page size for pagination. The maximum page size value is obtained from P and L report metadata API."
								}
							]
						},
						"description": "This API gives the data of the realised Profit and Loss report requested by a user"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/data?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>&page_number=1&page_size=3000",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"data"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										},
										{
											"key": "page_number",
											"value": "1"
										},
										{
											"key": "page_size",
											"value": "3000"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"data\": [\n    {\n      \"quantity\": 100,\n      \"isin\": \"INE256A01028\",\n      \"scrip_name\": \"ZEE ENTER\",\n      \"trade_type\": \"EQ\",\n      \"buy_date\": \"14-09-2021\",\n      \"buy_average\": 12345.67,\n      \"sell_date\": \"14-09-2021\",\n      \"sell_average\": 12345.67,\n      \"buy_amount\": 12345.67,\n      \"sell_amount\": 12345.67\n    },\n    {\n      \"quantity\": 100,\n      \"isin\": \"INE256A01028\",\n      \"scrip_name\": \"ZEE ENTER\",\n      \"trade_type\": \"EQ\",\n      \"buy_date\": \"14-09-2021\",\n      \"buy_average\": 12345.67,\n      \"sell_date\": \"14-09-2021\",\n      \"sell_average\": 12345.67,\n      \"buy_amount\": 12345.67,\n      \"sell_amount\": 12345.67\n    }\n  ],\n  \"metadata\": {\n    \"page\": {\n      \"page_number\": 1,\n      \"page_size\": 2\n    }\n  }\n}"
						},
						{
							"name": "UDAPI1070 - The financial_year is required<br>UDAPI1071 - The page_number is required<br>UDAPI1072 - The page_size is required<br>UDAPI1067 - The ''segment'' is required<br>UDAPI1066 - The ''segment'' is invalid<br>UDAPI1073 - Financial year should have m",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/data?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>&page_number=1&page_size=3000",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"data"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										},
										{
											"key": "page_number",
											"value": "1"
										},
										{
											"key": "page_size",
											"value": "3000"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/data?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>&page_number=1&page_size=3000",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"data"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										},
										{
											"key": "page_number",
											"value": "1"
										},
										{
											"key": "page_size",
											"value": "3000"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/data?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>&page_number=1&page_size=3000",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"data"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										},
										{
											"key": "page_number",
											"value": "1"
										},
										{
											"key": "page_size",
											"value": "3000"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/data?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>&page_number=1&page_size=3000",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"data"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										},
										{
											"key": "page_number",
											"value": "1"
										},
										{
											"key": "page_size",
											"value": "3000"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/data?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>&page_number=1&page_size=3000",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"data"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										},
										{
											"key": "page_number",
											"value": "1"
										},
										{
											"key": "page_size",
											"value": "3000"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				},
				{
					"name": "Get profit and loss on trades",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/trade/profit-loss/charges?from_date=<string>&to_date=<string>&segment=<string>&financial_year=<string>",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"trade",
								"profit-loss",
								"charges"
							],
							"query": [
								{
									"key": "from_date",
									"value": "<string>",
									"description": "Date from which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format"
								},
								{
									"key": "to_date",
									"value": "<string>",
									"description": "Date till which data needs to be fetched. from_date and to_date should fall under the same financial year as mentioned in financial_year attribute. Date in dd-mm-yyyy format"
								},
								{
									"key": "segment",
									"value": "<string>",
									"description": "(Required) Segment for which data is requested can be from the following options EQ - Equity,   FO - Futures and Options,   COM  - Commodity,   CD - Currency Derivatives"
								},
								{
									"key": "financial_year",
									"value": "<string>",
									"description": "(Required) Financial year for which data has been requested. Concatenation of last 2 digits of from year and to year Sample:for 2021-2022, financial_year will be 2122"
								}
							]
						},
						"description": "This API gives the charges incurred by users for their trades"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/charges?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"charges"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": {\n    \"charges_breakdown\": {\n      \"total\": 123.1,\n      \"brokerage\": 432.1,\n      \"taxes\": {\n        \"gst\": -65501828.677648224,\n        \"stt\": 67916071.94582716,\n        \"stamp_duty\": 84397591.18390593\n      },\n      \"charges\": {\n        \"transaction\": 82103018.53164572,\n        \"clearing\": 44569717.275550544,\n        \"others\": -54154128.374533616,\n        \"sebi_turnover\": 71995218.80821645,\n        \"demat_transaction\": -10815990.6493337\n      }\n    }\n  }\n}"
						},
						{
							"name": "UDAPI1067 - The ''segment'' is required<br>UDAPI1066 - The ''segment'' is invalid<br>UDAPI1068 - The start_date is required<br>UDAPI1069 - The end_date is required",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/charges?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"charges"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/charges?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"charges"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/charges?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"charges"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/charges?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"charges"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/trade/profit-loss/charges?from_date=01-04-2022&to_date=31-03-2023&segment=EQ&financial_year=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"trade",
										"profit-loss",
										"charges"
									],
									"query": [
										{
											"key": "from_date",
											"value": "01-04-2022"
										},
										{
											"key": "to_date",
											"value": "31-03-2023"
										},
										{
											"key": "segment",
											"value": "EQ"
										},
										{
											"key": "financial_year",
											"value": "<string>"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				}
			]
		},
		{
			"name": "History",
			"item": [
				{
					"name": "{instrument Key}/{interval}/{to date}",
					"item": [
						{
							"name": "Historical candle data",
							"request": {
								"auth": {
									"type": "bearer",
									"bearer": [
										{
											"key": "token",
											"value": "{{accessToken}}",
											"type": "string"
										}
									]
								},
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "{{version}}"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"historical-candle",
										":instrumentKey",
										":interval",
										":to_date"
									],
									"variable": [
										{
											"key": "instrumentKey",
											"value": "NSE_EQ%7CINE848E01016",
											"description": "(Required) "
										},
										{
											"key": "interval",
											"value": "month",
											"description": "(Required) "
										},
										{
											"key": "to_date",
											"value": "2023-09-01",
											"description": "(Required) "
										}
									]
								},
								"description": "Get OHLC values for all instruments across various timeframes. Historical data can be fetched for the following durations.\n1minute: last 1 month candles till endDate\n30minute: last 1 year candles till endDate\nday: last 1 year candles till endDate\nweek: last 10 year candles till endDate\nmonth: last 10 year candles till endDate"
							},
							"response": [
								{
									"name": "Successful",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"status\": \"success\",\n  \"data\": {\n    \"candles\": [\n      [],\n      []\n    ]\n  }\n}"
								},
								{
									"name": "UDAPI1015 - to_date must be greater than or equal to from_date and Date should be in valid format: yyyy-mm-dd<br>UDAPI1020 - Interval accepts one of (1minute,30minute,day,week,month)<br>UDAPI1021 - Instrument key is of invalid format<br>UDAPI1022 - to_dat",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Bad Request",
									"code": 400,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
								},
								{
									"name": "Unauthorized",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Unauthorized",
									"code": 401,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Method Not Allowed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Method Not Allowed",
									"code": 405,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Too Many Requests",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Too Many Requests",
									"code": 429,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Internal Server Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Internal Server Error",
									"code": 500,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								}
							]
						},
						{
							"name": "Historical candle data",
							"request": {
								"auth": {
									"type": "bearer",
									"bearer": [
										{
											"key": "token",
											"value": "{{accessToken}}",
											"type": "string"
										}
									]
								},
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "{{version}}"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date/:from_date",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"historical-candle",
										":instrumentKey",
										":interval",
										":to_date",
										":from_date"
									],
									"variable": [
										{
											"key": "instrumentKey",
											"value": "NSE_EQ%7CINE848E01016",
											"description": "(Required) "
										},
										{
											"key": "interval",
											"value": "day",
											"description": "(Required) "
										},
										{
											"key": "to_date",
											"value": "2023-09-03",
											"description": "(Required) "
										},
										{
											"key": "from_date",
											"value": "2023-09-01",
											"description": "(Required) "
										}
									]
								},
								"description": "Get OHLC values for all instruments across various timeframes. Historical data can be fetched for the following durations.\n1minute: last 1 month candles till endDate\n30minute: last 1 year candles till endDate\nday: last 1 year candles till endDate\nweek: last 10 year candles till endDate\nmonth: last 10 year candles till endDate"
							},
							"response": [
								{
									"name": "Successful",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date/:from_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date",
												":from_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "from_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"status\": \"success\",\n  \"data\": {\n    \"candles\": [\n      [],\n      []\n    ]\n  }\n}"
								},
								{
									"name": "UDAPI1015 - to_date must be greater than or equal to from_date and Date should be in valid format: yyyy-mm-dd<br>UDAPI1020 - Interval accepts one of (1minute,30minute,day,week,month)<br>UDAPI1021 - Instrument key is of invalid format<br>UDAPI1022 - to_dat",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date/:from_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date",
												":from_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "from_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Bad Request",
									"code": 400,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
								},
								{
									"name": "Unauthorized",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date/:from_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date",
												":from_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "from_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Unauthorized",
									"code": 401,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Method Not Allowed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date/:from_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date",
												":from_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "from_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Method Not Allowed",
									"code": 405,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Too Many Requests",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date/:from_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date",
												":from_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "from_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Too Many Requests",
									"code": 429,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Internal Server Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/historical-candle/:instrumentKey/:interval/:to_date/:from_date",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"historical-candle",
												":instrumentKey",
												":interval",
												":to_date",
												":from_date"
											],
											"variable": [
												{
													"key": "instrumentKey",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "interval",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "to_date",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "from_date",
													"value": "<string>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Internal Server Error",
									"code": 500,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								}
							]
						}
					]
				},
				{
					"name": "Intra day candle data",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/historical-candle/intraday/:instrumentKey/:interval",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"historical-candle",
								"intraday",
								":instrumentKey",
								":interval"
							],
							"variable": [
								{
									"key": "instrumentKey",
									"value": "NSE_EQ%7CINE848E01016",
									"description": "(Required) "
								},
								{
									"key": "interval",
									"value": "30minute",
									"description": "(Required) "
								}
							]
						},
						"description": "Get OHLC values for all instruments for the present trading day"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/historical-candle/intraday/:instrumentKey/:interval",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"historical-candle",
										"intraday",
										":instrumentKey",
										":interval"
									],
									"variable": [
										{
											"key": "instrumentKey",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "interval",
											"value": "<string>",
											"description": "(Required) "
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"data\": {\n    \"candles\": [\n      [],\n      []\n    ]\n  }\n}"
						},
						{
							"name": "UDAPI1076 - Interval accepts one of (1minute,30minute)<br>UDAPI1021 - Instrument key is of invalid format<br>UDAPI100011 - Invalid Instrument key",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/historical-candle/intraday/:instrumentKey/:interval",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"historical-candle",
										"intraday",
										":instrumentKey",
										":interval"
									],
									"variable": [
										{
											"key": "instrumentKey",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "interval",
											"value": "<string>",
											"description": "(Required) "
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/historical-candle/intraday/:instrumentKey/:interval",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"historical-candle",
										"intraday",
										":instrumentKey",
										":interval"
									],
									"variable": [
										{
											"key": "instrumentKey",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "interval",
											"value": "<string>",
											"description": "(Required) "
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/historical-candle/intraday/:instrumentKey/:interval",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"historical-candle",
										"intraday",
										":instrumentKey",
										":interval"
									],
									"variable": [
										{
											"key": "instrumentKey",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "interval",
											"value": "<string>",
											"description": "(Required) "
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/historical-candle/intraday/:instrumentKey/:interval",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"historical-candle",
										"intraday",
										":instrumentKey",
										":interval"
									],
									"variable": [
										{
											"key": "instrumentKey",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "interval",
											"value": "<string>",
											"description": "(Required) "
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/historical-candle/intraday/:instrumentKey/:interval",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"historical-candle",
										"intraday",
										":instrumentKey",
										":interval"
									],
									"variable": [
										{
											"key": "instrumentKey",
											"value": "<string>",
											"description": "(Required) "
										},
										{
											"key": "interval",
											"value": "<string>",
											"description": "(Required) "
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				}
			]
		},
		{
			"name": "Charge",
			"item": [
				{
					"name": "Brokerage details",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "{{accessToken}}",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [
							{
								"description": "(Required) API Version Header",
								"key": "Api-Version",
								"value": "{{version}}"
							},
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": {
							"raw": "{{baseUrl}}/charges/brokerage?instrument_token=NSE_EQ|INE848E01016&quantity=10&product=I&transaction_type=BUY&price=123.1",
							"host": [
								"{{baseUrl}}"
							],
							"path": [
								"charges",
								"brokerage"
							],
							"query": [
								{
									"key": "instrument_token",
									"value": "NSE_EQ|INE848E01016",
									"description": "(Required) Key of the instrument"
								},
								{
									"key": "quantity",
									"value": "10",
									"description": "(Required) Quantity with which the order is to be placed"
								},
								{
									"key": "product",
									"value": "I",
									"description": "(Required) Product with which the order is to be placed"
								},
								{
									"key": "transaction_type",
									"value": "BUY",
									"description": "(Required) Indicates whether its a BUY or SELL order"
								},
								{
									"key": "price",
									"value": "123.1",
									"description": "(Required) Price with which the order is to be placed"
								}
							]
						},
						"description": "Compute Brokerage Charges"
					},
					"response": [
						{
							"name": "Successful",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/charges/brokerage?instrument_token=NSE_EQ|INE848E01016&quantity=10&product=I&transaction_type=BUY&price=123.1",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"charges",
										"brokerage"
									],
									"query": [
										{
											"key": "instrument_token",
											"value": "NSE_EQ|INE848E01016"
										},
										{
											"key": "quantity",
											"value": "10"
										},
										{
											"key": "product",
											"value": "I"
										},
										{
											"key": "transaction_type",
											"value": "BUY"
										},
										{
											"key": "price",
											"value": "123.1"
										}
									]
								}
							},
							"status": "OK",
							"code": 200,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"error\",\n  \"data\": {\n    \"charges\": {\n      \"total\": 55745105.54463473,\n      \"brokerage\": -92647693.48616247,\n      \"taxes\": {\n        \"gst\": 59806391.639532864,\n        \"stt\": 943946.4081138372,\n        \"stamp_duty\": -54710161.48351135\n      },\n      \"otherTaxes\": {\n        \"transaction\": -18674814.04710616,\n        \"clearing\": 91206329.26003882,\n        \"sebi_turnover\": 94288088.19046196\n      },\n      \"dpPlan\": {\n        \"name\": \"labore ex Excepteur proident\",\n        \"min_expense\": -55769658.71419581\n      }\n    }\n  }\n}"
						},
						{
							"name": "UDAPI1060 - The quantity is required<br>UDAPI1061 - The price is required<br>UDAPI1062 - The transaction_type is required<br> UDAPI1063 - The product is required<br> UDAPI1064 - The quantity cannot be zero<br>UDAPI1065 - The price cannot be zero<br>UDAPI1",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/charges/brokerage?instrument_token=NSE_EQ|INE848E01016&quantity=10&product=I&transaction_type=BUY&price=123.1",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"charges",
										"brokerage"
									],
									"query": [
										{
											"key": "instrument_token",
											"value": "NSE_EQ|INE848E01016"
										},
										{
											"key": "quantity",
											"value": "10"
										},
										{
											"key": "product",
											"value": "I"
										},
										{
											"key": "transaction_type",
											"value": "BUY"
										},
										{
											"key": "price",
											"value": "123.1"
										}
									]
								}
							},
							"status": "Bad Request",
							"code": 400,
							"_postman_previewlanguage": "json",
							"header": [
								{
									"key": "Content-Type",
									"value": "application/json"
								}
							],
							"cookie": [],
							"body": "{\n  \"status\": \"success\",\n  \"errors\": [\n    {\n      \"errorCode\": \"aute reprehenderit fugiat dolore\",\n      \"message\": \"culpa\",\n      \"propertyPath\": \"et commodo\",\n      \"invalidValue\": {},\n      \"error_code\": \"aliqua dolor\",\n      \"property_path\": \"e\",\n      \"invalid_value\": {}\n    },\n    {\n      \"errorCode\": \"sint laboris cupidatat\",\n      \"message\": \"ipsum ea\",\n      \"propertyPath\": \"elit pariatur sed dolore\",\n      \"invalidValue\": {},\n      \"error_code\": \"Lorem dolor irure in pariatur\",\n      \"property_path\": \"irure occaecat\",\n      \"invalid_value\": {}\n    }\n  ]\n}"
						},
						{
							"name": "Unauthorized",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/charges/brokerage?instrument_token=NSE_EQ|INE848E01016&quantity=10&product=I&transaction_type=BUY&price=123.1",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"charges",
										"brokerage"
									],
									"query": [
										{
											"key": "instrument_token",
											"value": "NSE_EQ|INE848E01016"
										},
										{
											"key": "quantity",
											"value": "10"
										},
										{
											"key": "product",
											"value": "I"
										},
										{
											"key": "transaction_type",
											"value": "BUY"
										},
										{
											"key": "price",
											"value": "123.1"
										}
									]
								}
							},
							"status": "Unauthorized",
							"code": 401,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Method Not Allowed",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/charges/brokerage?instrument_token=NSE_EQ|INE848E01016&quantity=10&product=I&transaction_type=BUY&price=123.1",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"charges",
										"brokerage"
									],
									"query": [
										{
											"key": "instrument_token",
											"value": "NSE_EQ|INE848E01016"
										},
										{
											"key": "quantity",
											"value": "10"
										},
										{
											"key": "product",
											"value": "I"
										},
										{
											"key": "transaction_type",
											"value": "BUY"
										},
										{
											"key": "price",
											"value": "123.1"
										}
									]
								}
							},
							"status": "Method Not Allowed",
							"code": 405,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Too Many Requests",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/charges/brokerage?instrument_token=NSE_EQ|INE848E01016&quantity=10&product=I&transaction_type=BUY&price=123.1",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"charges",
										"brokerage"
									],
									"query": [
										{
											"key": "instrument_token",
											"value": "NSE_EQ|INE848E01016"
										},
										{
											"key": "quantity",
											"value": "10"
										},
										{
											"key": "product",
											"value": "I"
										},
										{
											"key": "transaction_type",
											"value": "BUY"
										},
										{
											"key": "price",
											"value": "123.1"
										}
									]
								}
							},
							"status": "Too Many Requests",
							"code": 429,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						},
						{
							"name": "Internal Server Error",
							"originalRequest": {
								"method": "GET",
								"header": [
									{
										"description": "Added as a part of security scheme: oauth2",
										"key": "Authorization",
										"value": "<token>"
									},
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "<string>"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/charges/brokerage?instrument_token=NSE_EQ|INE848E01016&quantity=10&product=I&transaction_type=BUY&price=123.1",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"charges",
										"brokerage"
									],
									"query": [
										{
											"key": "instrument_token",
											"value": "NSE_EQ|INE848E01016"
										},
										{
											"key": "quantity",
											"value": "10"
										},
										{
											"key": "product",
											"value": "I"
										},
										{
											"key": "transaction_type",
											"value": "BUY"
										},
										{
											"key": "price",
											"value": "123.1"
										}
									]
								}
							},
							"status": "Internal Server Error",
							"code": 500,
							"_postman_previewlanguage": "text",
							"header": [
								{
									"key": "Content-Type",
									"value": "*/*"
								}
							],
							"cookie": [],
							"body": ""
						}
					]
				}
			]
		},
		{
			"name": "Websocket",
			"item": [
				{
					"name": "portfolio-stream-feed",
					"item": [
						{
							"name": "Portfolio Stream Feed",
							"request": {
								"auth": {
									"type": "bearer",
									"bearer": [
										{
											"key": "token",
											"value": "{{accessToken}}",
											"type": "string"
										}
									]
								},
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "{{version}}"
									},
									{
										"key": "Accept",
										"value": "*/*"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/feed/portfolio-stream-feed",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"feed",
										"portfolio-stream-feed"
									]
								},
								"description": "This API redirects the client to the respective socket endpoint to receive Portfolio updates."
							},
							"response": [
								{
									"name": "Location for authorized access of portfolio stream feed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed"
											]
										}
									},
									"status": "Found",
									"code": 302,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "text/plain"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Bad Request",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed"
											]
										}
									},
									"status": "Bad Request",
									"code": 400,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Unauthorized",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed"
											]
										}
									},
									"status": "Unauthorized",
									"code": 401,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Method Not Allowed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed"
											]
										}
									},
									"status": "Method Not Allowed",
									"code": 405,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Too Many Requests",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed"
											]
										}
									},
									"status": "Too Many Requests",
									"code": 429,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Internal Server Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed"
											]
										}
									},
									"status": "Internal Server Error",
									"code": 500,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								}
							]
						},
						{
							"name": "Portfolio Stream Feed Authorize",
							"request": {
								"auth": {
									"type": "bearer",
									"bearer": [
										{
											"key": "token",
											"value": "{{accessToken}}",
											"type": "string"
										}
									]
								},
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "{{version}}"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/feed/portfolio-stream-feed/authorize",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"feed",
										"portfolio-stream-feed",
										"authorize"
									]
								},
								"description": " This API provides the functionality to retrieve the socket endpoint URI for Portfolio updates."
							},
							"response": [
								{
									"name": "Successful",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed",
												"authorize"
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"status\": \"error\",\n  \"data\": {\n    \"authorizedRedirectUri\": \"irure aliqua sit dolor\"\n  }\n}"
								},
								{
									"name": "Bad Request",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed",
												"authorize"
											]
										}
									},
									"status": "Bad Request",
									"code": 400,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Unauthorized",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed",
												"authorize"
											]
										}
									},
									"status": "Unauthorized",
									"code": 401,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Method Not Allowed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed",
												"authorize"
											]
										}
									},
									"status": "Method Not Allowed",
									"code": 405,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Too Many Requests",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed",
												"authorize"
											]
										}
									},
									"status": "Too Many Requests",
									"code": 429,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Internal Server Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/portfolio-stream-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"portfolio-stream-feed",
												"authorize"
											]
										}
									},
									"status": "Internal Server Error",
									"code": 500,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								}
							]
						}
					]
				},
				{
					"name": "market-data-feed",
					"item": [
						{
							"name": "Market Data Feed",
							"request": {
								"auth": {
									"type": "bearer",
									"bearer": [
										{
											"key": "token",
											"value": "{{accessToken}}",
											"type": "string"
										}
									]
								},
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "{{version}}"
									},
									{
										"key": "Accept",
										"value": "*/*"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/feed/market-data-feed",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"feed",
										"market-data-feed"
									]
								},
								"description": " This API redirects the client to the respective socket endpoint to receive Market updates."
							},
							"response": [
								{
									"name": "Location for authorized access of market data feed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed"
											]
										}
									},
									"status": "Found",
									"code": 302,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "text/plain"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Bad Request",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed"
											]
										}
									},
									"status": "Bad Request",
									"code": 400,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Unauthorized",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed"
											]
										}
									},
									"status": "Unauthorized",
									"code": 401,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Method Not Allowed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed"
											]
										}
									},
									"status": "Method Not Allowed",
									"code": 405,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Too Many Requests",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed"
											]
										}
									},
									"status": "Too Many Requests",
									"code": 429,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Internal Server Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed"
											]
										}
									},
									"status": "Internal Server Error",
									"code": 500,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								}
							]
						},
						{
							"name": "Market Data Feed Authorize",
							"request": {
								"auth": {
									"type": "bearer",
									"bearer": [
										{
											"key": "token",
											"value": "{{accessToken}}",
											"type": "string"
										}
									]
								},
								"method": "GET",
								"header": [
									{
										"description": "(Required) API Version Header",
										"key": "Api-Version",
										"value": "{{version}}"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/feed/market-data-feed/authorize",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"feed",
										"market-data-feed",
										"authorize"
									]
								},
								"description": "This API provides the functionality to retrieve the socket endpoint URI for Market updates."
							},
							"response": [
								{
									"name": "Successful",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed",
												"authorize"
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"status\": \"error\",\n  \"data\": {\n    \"authorizedRedirectUri\": \"irure aliqua sit dolor\"\n  }\n}"
								},
								{
									"name": "Bad Request",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed",
												"authorize"
											]
										}
									},
									"status": "Bad Request",
									"code": 400,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Unauthorized",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed",
												"authorize"
											]
										}
									},
									"status": "Unauthorized",
									"code": 401,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Method Not Allowed",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed",
												"authorize"
											]
										}
									},
									"status": "Method Not Allowed",
									"code": 405,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Too Many Requests",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed",
												"authorize"
											]
										}
									},
									"status": "Too Many Requests",
									"code": 429,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								},
								{
									"name": "Internal Server Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"description": "Added as a part of security scheme: oauth2",
												"key": "Authorization",
												"value": "<token>"
											},
											{
												"description": "(Required) API Version Header",
												"key": "Api-Version",
												"value": "<string>"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/feed/market-data-feed/authorize",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"feed",
												"market-data-feed",
												"authorize"
											]
										}
									},
									"status": "Internal Server Error",
									"code": 500,
									"_postman_previewlanguage": "text",
									"header": [
										{
											"key": "Content-Type",
											"value": "*/*"
										}
									],
									"cookie": [],
									"body": ""
								}
							]
						}
					]
				}
			]
		}
	],
	"event": [
		{
			"listen": "prerequest",
			"script": {
				"type": "text/javascript",
				"exec": [
					""
				]
			}
		},
		{
			"listen": "test",
			"script": {
				"type": "text/javascript",
				"exec": [
					""
				]
			}
		}
	],
	"variable": [
		{
			"key": "baseUrl",
			"value": "https://api-v2.upstox.com",
			"type": "string"
		},
		{
			"key": "accessToken",
			"value": ""
		},
		{
			"key": "version",
			"value": "2.0",
			"type": "string"
		}
	]
}