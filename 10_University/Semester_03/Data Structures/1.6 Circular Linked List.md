This is an extension of regular linked lists, with the only difference being that the last element points back to the head. This changes the structure of Node and the List class in a few ways.
### Node:

```cpp
// NODE 
template<typename T>
struct Node{
	T data;
	Node* next;
	Node(const T& value): data(value), next(*this) {}
};

```

### List
```cpp
template<typename T>
class CircularList{
	Node* head;
public:
	CircularList(): head(nullptr) {}
};
```
### Push back
```cpp
void push_back(const T& value) {
	Node<T>* newNode = new Node<T>(value);
	if (!head) {
		head = newNode;
	} else {
		Node<T>* tail = head;
		while (tail->next != head) {
			tail = tail->next;
		}
		tail->next = newNode;
		newNode->next = head;
	}
}
```
