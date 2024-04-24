# gpt-cam

A little program to demonstrate how you could use the OpenAI API to analyze video feeds
(in this case, the local webcam) and feed the result to a GPT function call.

## Requrements

 * Python3
 * OpenCV
 * The OpenAI Python library
 * A webcam

## Usage

echo "YOUR_OPEN_AI_KEY" > key.txt
./run.py "statement prompt" "parameter name 0" "parameter description 0" "parameter data type 0" [...]

## Example

./run.py "State the severity of any accident in the image, if any" "severity" "how severe the situation is, from 0 to 10" "integer" "type" "the type of accident" "string"
