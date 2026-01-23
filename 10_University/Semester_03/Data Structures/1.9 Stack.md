## Array Based
```cpp
class Stack {
    int* arr;
    int capacity;
    int topIndex;

public:
    // Constructor
    Stack(int c = 5) {
        capacity = c;
        arr = new int[capacity];
        topIndex = -1;
    }

    // Destructor
    ~Stack() {
        delete[] arr;
    }

    // Push operation
    void push(int value) {
        if (isFull()) {
            cout << "Stack Overflow! Cannot push " << value << endl;
            return;
        }
        arr[++topIndex] = value;
    }

    // Pop operation
    int pop() {
        if (isEmpty()) {
            cout << "Stack Underflow! Cannot pop." << endl;
            return -1;
        }
        return arr[topIndex--];
    }

    // Peek top element
    int top() const {
        if (isEmpty()) {
            cout << "Stack is empty!" << endl;
            return -1;
        }
        return arr[topIndex];
    }

    // Check empty/full
    bool isEmpty() const {
        return topIndex == -1;
    }

    bool isFull() const {
        return topIndex == capacity - 1;
    }

    // Display
    void display() const {
        if (isEmpty()) {
            cout << "Stack is empty!" << endl;
            return;
        }
        cout << "Stack (top → bottom): ";
        for (int i = topIndex; i >= 0; i--)
            cout << arr[i] << " ";
        cout << endl;
    }
};
```

## Linked List Based
```cpp
class Node {
	int data;
	Node* next;
	
	Node(int d): data(d), next(nullptr) {}
	
};
```