#!/usr/bin/env python3

import os, sys, time, json
import base64
import openai
from openai import OpenAI
import cv2
import imutils

api_key = open("key.txt", "r").read().strip()
client = OpenAI(api_key=api_key)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

def analyze(instruction, args, img):
    cv2.imwrite("/tmp/img.jpg", img)
    imgdata = open("/tmp/img.jpg", "rb").read()
    b64data = base64.b64encode(imgdata).decode('utf-8')

    message_content = [
        {
            "type": "text",
            "text": instruction,
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{b64data}",
                "detail": "low",
            },
        }
    ]
    messages = [{"role": "user", "content": message_content}]

    function_args = {}
    required = []
    for arg in args:
        function_args[arg["name"]] = {
            "type": arg["type"],
            "description": arg["desc"],
        }
        required.append(arg["name"])

    tool = {
        "type": "function",
        "function": {
            "name": "report",
            "description": "report",
            "parameters": {
                "type": "object",
                "properties": function_args,
                "required": required,
            },
        },
    }

    tool_choice = {
        "type": "function",
        "function": { "name": "report" },
    }

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        tools=[tool],
        tool_choice=tool_choice,
        max_tokens=128,
    )

    call_args = response.choices[0].message.tool_calls[0].function.arguments
    call_args = json.loads(call_args)

    retv = []
    for arg in call_args:
        val = call_args[arg] 
        retv.append((arg, val))

    return retv

instruction = sys.argv[1]
args = sys.argv[2:]
args = [args[n:n+3] for n in range(0, len(args), 3)]
func_args = []
for arg in args:
    func_args.append({
    "name": arg[0],
    "desc": arg[1],
    "type": arg[2],
})

while True:
    ret, frame = cam.read()
    frame = imutils.resize(frame, height=512)
    wp = (frame.shape[1]-512)//2
    frame = frame[0:512,wp:wp+512]

    result = analyze(instruction, func_args, frame)
    print("---")
    for res in result:
        print(res[0], ": ", res[1], sep='')

    # just drain frames
    ts_start = time.time()
    while (time.time() - ts_start) < 1.0:
        ret, frame = cam.read()
