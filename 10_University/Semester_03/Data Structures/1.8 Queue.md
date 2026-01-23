## Array Based
Uses an array to implement a Queue.

```cpp
class Queue {
    int* array;
    int capacity;
    int size;
    int front;
    int rear;

public:
    // Constructor
    Queue(int c = 2) {
        capacity = c;
        array = new int[capacity];
        size = 0;
        front = 0;
        rear = -1;
    }

    // Destructor
    ~Queue() {
        delete[] array;
    }

    // Enqueue operation
    void enqueue(int value) {
        if (isFull()) {
            cout << "Queue is full! Cannot enqueue " << value << endl;
            return;
        }
        rear = (rear + 1) % capacity;
        array[rear] = value;
        size++;
    }

    // Dequeue operation
    int dequeue() {
        if (isEmpty()) {
            cout << "Queue is empty! Cannot dequeue." << endl;
            return -1; // sentinel value
        }
        int value = array[front];
        front = (front + 1) % capacity;
        size--;
        return value;
    }

    // Peek front element
    int peek() const {
        if (isEmpty()) {
            cout << "Queue is empty!" << endl;
            return -1;
        }
        return array[front];
    }

    // Check if queue is empty
    bool isEmpty() const {
        return size == 0;
    }

    // Check if queue is full
    bool isFull() const {
        return size == capacity;
    }

    // Get current size
    int getSize() const {
        return size;
    }

    // Display all elements
    void display() const {
        if (isEmpty()) {
            cout << "Queue is empty!" << endl;
            return;
        }
        cout << "Queue elements: ";
        for (int i = 0; i < size; i++) {
            cout << array[(front + i) % capacity] << " ";
        }
        cout << endl;
    }
};
```

## Linked List based Queue
Implemented using a linked list.

```cpp
class Node {
	int val;
	Node* next;
	
	Node(int val) : val(val), next(nullptr) {}
};

class Queue {
	Node* head;
	Node* tail;
	int capacity;
	int size;
	
public:
	Queue(int c = 10) : head(nullptr), tail(nullptr), capacity(c), size(0) {}
	~Queue() {
		Node* curr = head;
		while(curr) {
			Node* toDel = curr;
			curr = curr->next;
			delete toDel;
		}
	}
	
	bool isFull() {
		return size == capacity;
	}
	
	bool isEmpty() {
		return head == nullptr;
	}
	
	void enqueue(int val) {
		if(isFull()) {
			cout<<"FULL..."<<endl;
			return;
		}
		
		if(!head) {
			head = tail = new Node(val);
		}
		else {
			Node* newNode = new Node(val);
			tail->next = newNode;
			tail = newNode;
		}
	} 
	
	int dequeue() {
		if(isEmpty()) {
			cout<<"EMPTY..."<<endl;
			return;
		}
		Node* toDel = head;
		head = head->next;
		int val = toDel->val;
		delete toDel;
		return val;
	}
};
```