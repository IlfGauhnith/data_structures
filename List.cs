using System;

namespace data_structures_with_CSharp
{

    internal class ListNode<T> 
    {
        internal T data;
        internal ListNode<T> previous;
        internal ListNode<T> next;
        internal int index;
    }
    public class List<T>
    {
        // This is a circular doubly linked list.

        private int size;
        private ListNode<T> first;
        private ListNode<T> last;
        
        public List() {
            this.size = 0;
            this.first = new ListNode<T>();
            this.last = first;

            this.first.next = this.first;
            this.first.previous = this.last;
        }

        public void add(T newItem) {
            // insert at the end of the list.
            
            if (newItem is null) {
                throw new ArgumentNullException($"List dont accept null data. {nameof(newItem)} is null");
            }
            
            if (this.size == 0) {
                this.first.data = newItem;
                this.size++;
                this.first.index = size;
            } else {
                ListNode<T> newNode = new ListNode<T>();
                newNode.data = newItem;
                newNode.previous = this.last;
                newNode.next = this.first;

                this.last.next = newNode;
                this.first.previous = newNode;
                
                this.last = newNode;

                size++;
                this.last.index = size;
            }
        }

        public T remove() {
            // return list's last element.

            if (size == 0) throw new InvalidOperationException("List is empty.");

            T ret = this.last.data;

            // fixing circularity
            this.last.previous.next = this.first;
            this.first.previous = this.last.previous;

            this.last = this.last.previous;
            size--;

            if (size == 0) {
                this.clearList();
            }
            
            return ret;
        }
        public T remove(int index) {
            if (size == 0) throw new InvalidOperationException("List is empty.");
            else if (index < 1 || index > this.size) throw new IndexOutOfRangeException($"{index} is out of list bounds");
            
            void fixIndexing(int index) {
                ListNode<T> currentNode = first;
                for (int i = 1 ; i <= this.size ; i++) {
                    if (currentNode.index > index) currentNode.index = currentNode.index - 1;
                    currentNode = currentNode.next;
                }
            }

            T ret = default(T);
            
            if (size == 1) {
                ret = this.first.data;
                size--;
                this.clearList();

            } else if (index == 1) {
                ret = this.first.data;

                // fixing circularity
                this.first.next.previous = this.last;
                this.last.next = this.first.next;
                
                this.first = this.first.next;
                size--;

                fixIndexing(index);
                if (size == 1) {
                    this.last = this.first;
                }

            } else if (index == this.size) {
                ret = this.last.data;
                
                // fixing circularity
                this.last.previous.next = this.first;
                this.first.previous = this.last.previous;

                this.last = this.last.previous;
                size--;

                if (size == 1) {
                    this.first = this.last;
                }

            } else {
                ListNode<T> currentNode;
                if (index > this.size/2) {
                    currentNode = this.last.previous;
                    for (int i = this.size-1 ; i > this.size/2 ; i--) {
                        if(currentNode.index == index) break;
                        currentNode = currentNode.previous;
                    }
                } else {
                    currentNode = this.first.next;
                    for (int i = 2 ; i <= this.size/2 ; i++) {
                        if(currentNode.index == index) break;
                        currentNode = currentNode.next;
                    }
                }

                ret = currentNode.data;

                currentNode.previous.next = currentNode.next;
                currentNode.next.previous = currentNode.previous;

                size--;
                fixIndexing(index);
            }
            return ret;
        }

        public T search(int index) {
            if (size == 0) throw new InvalidOperationException("List is empty.");
            else if (index < 1 || index > this.size) throw new IndexOutOfRangeException($"{index} is out of list bounds");
            
            if (index == 1) return this.first.data;
            else if (index == this.size) return this.last.data;
            
            ListNode<T> currentNode;
            if (index > this.size/2) {
                currentNode = this.last.previous;
                for (int i = this.size-1 ; i > this.size/2 ; i--) {
                    if(currentNode.index == index) return currentNode.data;
                    currentNode = currentNode.previous;
                }
            } else {
                currentNode = this.first.next;
                for (int i = 2 ; i <= this.size/2 ; i++) {
                    if(currentNode.index == index) return currentNode.data;
                    currentNode = currentNode.next;
                }
            }

            return default(T);
        }

        public void clearList() {
            this.first = new ListNode<T>();
            this.last = this.first;

            this.first.next = this.first;
            this.first.previous = this.last;
        }

        public override string ToString()
        {
            String res = "---- <> -- MY LIST -- <> ----\n";
            
            if (this.size == 0) return res + "empty";

            ListNode<T> currentNode = first;

            for(int i = 1 ; i <= this.size ; i++) 
            {
                if (i != this.size) res = res + $"[(data:{currentNode.data}), (index:{currentNode.index})] <----> ";
                else res = res + $"[(data:{currentNode.data}), (index:{currentNode.index})]";

                currentNode = currentNode.next;
            }

            return res;
        }
    }
}