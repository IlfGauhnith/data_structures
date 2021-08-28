using System;

namespace data_structures_with_CSharp
{
    internal class StackNode<T> 
    {
        internal T data;
        internal StackNode<T> previous;
        internal StackNode<T> next;
    }

    public class Stack<T>
    {
        private StackNode<T> top;
        private int size;

        public Stack() {
            this.top = new StackNode<T>();
            this.top.previous = top;
            this.top.next = top;

            this.size = 0;
        }

        public void push(T newItem) {
            if (newItem is null) {
                throw new ArgumentNullException($"Stack dont accept null data. {nameof(newItem)} is null");
            }

            if (this.size == 0) {
                // Stack is empty
                this.top.data = newItem;
                size++;
            } else {
                // Not empty
                StackNode<T> newNode = new StackNode<T>();
                newNode.data = newItem;
                newNode.previous = this.top;
                newNode.next = newNode;

                this.top.next = newNode;
                this.top = newNode;

                size++;
            }
        }

        public T pop() {
            if (this.size == 0) {
                throw new InvalidOperationException("Stack is empty, you cannot pop it.");
            }

            T res = this.top.data;
            this.top.previous.next = this.top.previous;
            this.top = this.top.previous;
            size--;

            if (this.size == 0) {
                // check if its the bottom
                this.top.data = default(T);
            }
            return res;
        }

        public override String ToString() {
            String res = "----<>-- MY STACK --<>----\n\n";
            StackNode<T> nav = top;

            if (this.size == 0) return res + "empty";

            while (true) 
            {
                res = res + $"{nav.data}\n";
                nav = nav.previous;
                if(nav.previous == nav) {
                    res = res + $"{nav.data}\n";
                    break;
                }
            }
            return res;
        }
    }
}