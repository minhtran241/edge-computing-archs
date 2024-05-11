# Edge computing models for IoT Analytics

This repository contains a collection of edge computing models for IoT analytics. The models are designed to help organizations understand the benefits of edge computing and how it can be used to process data from IoT devices more efficiently. Each model provides an overview of the architecture, advantages, and use cases for edge computing in IoT analytics.

The code supports the research paper's writing process. The code is written in Python. [Raspberry Pi](https://www.raspberrypi.org/) is used as nodes in the edge computing network to simulate the edge computing environment. The code is written in Python and uses the [socketio](https://python-socketio.readthedocs.io/en/latest/) library to communicate between the nodes.

## Models

### Model 1: Edge computing with multiple edge servers

### Overview

This model is based on the idea of having multiple edge servers that are connected to the cloud. The edge servers are responsible for processing data from IoT devices and sending the results to the cloud for further analysis. This model is suitable for scenarios where low latency is required and where the cloud may not be able to handle the volume of data generated by IoT devices. The edge servers can be distributed geographically to reduce latency and improve reliability.

![Model 1](images/model1.png)

### Current implementation

- Raspberry Pi 3 for IoT devices
- Raspberry Pi 4 for edge servers

#### Advantages

- Low latency: Data processing is done closer to the source, reducing the time it takes to get results. This is important for real-time applications.
- Scalability: The edge servers can be easily scaled up or down based on the volume of data being generated.
- Reliability: Having multiple edge servers improves reliability as there is no single point of failure.

## Usage

### Requirements

- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [Raspberry Pi](https://www.raspberrypi.org/) with Raspbian OS installed
- [SocketIO](https://python-socketio.readthedocs.io/en/latest/)

### Set up environment variables

Create a `.env` file in the root directory and follow the template created in the [`.env.example`](https://github.com/minhtran241/edge-computing-models/blob/main/.env.example) file.

```bash
CLOUD_ADDRESS=
NUM_EDGE_NODES=
EDGE_1_ADDRESS=
EDGE_2_ADDRESS=
EDGE_3_ADDRESS=
```

> Note: The `NUM_EDGE_NODES` variable is used to specify the number of edge servers in the network. The `EDGE_1_ADDRESS`, `EDGE_2_ADDRESS`, and `EDGE_3_ADDRESS` variables are used to specify the IP addresses of the edge servers. If you have more than three edge servers, you can add more variables following the same pattern.

### Run the code

To run the code, you need to start the servers in the following order:

1. Start the cloud server
2. Start the edge servers
3. Start the IoT devices

For all the servers, you can run the following command:

```bash
python trigger.py
```

This will require your input to specify the following parameters:

- The role of the device (IoT device, edge server or cloud)
  - Valid roles: `iot`, `edge`, `cloud`
- The device ID
- The algorithm code [See the list of available algorithms](#available-algorithms)
- Number of iterations

#### Input format

```
================
Available roles:
iot <id> <algo_code> <iterations>
edge <id>
cloud <id>
================
```

#### Available algorithms

| Algorithm | Code | Description |
| --- | --- | --- |
| Smith-Waterman | `sw` | A dynamic programming algorithm for sequence alignment |
| Tesseract OCR | `ocr` | An optical character recognition algorithm for text recognition |
| YOLOv8 | `yolo` | An object detection algorithm for image recognition |

## Contributors

- [Minh Tran](https://minhtran-nine.vercel.app): Research Assistant, Grand Valley State University
- [Dr. Xiang Cao](https://www.linkedin.com/in/xiang-cao-15183570/): Associate Professor, Grand Valley State University
