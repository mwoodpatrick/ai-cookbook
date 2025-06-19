# Gemini-api-integration

You can use your own virtual environment .
to set the gemini environment on your pc use this command on your command prompt

pip install -q -U google-generativeai

# (Quickstart: Generate text using the Vertex AI Gemini API)[https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal]
# The SDK always converts the inputs to the contents argument into list[types.Content]. 
# The following shows some common ways to provide your inputs.
# So the above contents example where a string is provided the SDK converts it into:
# [
#   types.UserContent(
#       parts=[
#           types.Part.from_text(text='Why is the sky blue?')
#       ]
#   )
# ]
#
# Where a types.UserContent is a subclass of types.Content, it sets the role field to be user.
#
# If you provide a list of strings then the SDK assumes these are 2 text parts, 
# it converts this into a single content, like the following:
#
#[
#   types.UserContent(
#    parts=[
#       types.Part.from_text(text='Why is the sky blue?'),
#       types.Part.from_text(text='Why is the cloud white?'),
#    ]
#   )
#]
#
# The SDK converts a function call part to a content with a model role:
# [
#   types.ModelContent(
#     parts=[
#       types.Part.from_function_call(
#         name='get_weather_by_location',
#         args={'location': 'Boston'}
#       )
#     ]
#   )
# ]
#
# Where a types.ModelContent is a subclass of types.Content, the role field in types.ModelContent is fixed to be model.
#
#
# Provide a list of function call parts
#
#    contents = [
#        types.Part.from_function_call(
#            name='get_weather_by_location',
#            args={'location': 'Boston'}
#        ),
#        types.Part.from_function_call(
#           name='get_weather_by_location',
#           args={'location': 'New York'}
#       ),
#   ]
#
# The SDK converts a list of function call parts to the a content with a model role:
#
# [
#types.ModelContent(
#    parts=[
#       types.Part.from_function_call(
#           name='get_weather_by_location',
#           args={'location': 'Boston'}
#       ),
#       types.Part.from_function_call(
#           name='get_weather_by_location',
#           args={'location': 'New York'}
#       )
#    ]
#)
#]
#
# Where a types.ModelContent is a subclass of types.Content, the role field in types.ModelContent is fixed to be model.
#
# Provide a non function call part
# contents = types.Part.from_uri(
#    file_uri: 'gs://generativeai-downloads/images/scones.jpg',
#    mime_type: 'image/jpeg',
#   )
# The SDK converts all non function call parts into a content with a user role.
#
#[
#    types.UserContent(parts=[
#        types.Part.from_uri(
#            file_uri: 'gs://generativeai-downloads/images/scones.jpg',
#            mime_type: 'image/jpeg',
#        )
#       ])
#]
#
# Provide a list of non function call parts
# from google.genai import types
# 
# contents = [
# types.Part.from_text('What is this image about?'),
# types.Part.from_uri(
#     file_uri: 'gs://generativeai-downloads/images/scones.jpg',
#     mime_type: 'image/jpeg',
# )
# ]
# The SDK will convert the list of parts into a content with a user role
# 
# [
# types.UserContent(
#     parts=[
#     types.Part.from_text('What is this image about?'),
#     types.Part.from_uri(
#         file_uri: 'gs://generativeai-downloads/images/scones.jpg',
#         mime_type: 'image/jpeg',
#     )
#     ]
# )
# ]
#
# Mix types in contents
# You can also provide a list of types.ContentUnion. 
# The SDK leaves items of types.Content as is, 
# it groups consecutive non function call parts into a single types.UserContent, 
# and it groups consecutive function call parts into a single types.ModelContent.
# 
# If you put a list within a list, the inner list can only contain types.PartUnion items. 
# The SDK will convert the inner list into a single types.UserContent.

