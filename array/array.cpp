#include <iostream>
#include <new>

using namespace std;

class Array{
    private: int capacity = 16;
    protected: int length = 0;
    private: int *array;

    public: Array(){
        array = new(nothrow) int[capacity];
        if(array == nullptr){
            cout<<"Failed"<<endl;
        }
    }

    void put(int index, int value){
        if (index < 0 || index >= length){
            throw "Index out of range";
        }
        *(array+index) = value;
        return;
    }

    int get(int index){
        if (index < 0 || index >= length){
            throw "Index out of range";
        }
        return *(array+index);
    }

    void resize(){
        capacity *= 2;
        int *newarray = new(nothrow) int[capacity];
        if(newarray == nullptr){
            cout<<"Failed to resize"<<endl;
            return;
        }
        for(int i = 0; i < length; i++){
            *(newarray+i) = *(array+i);
        }
        delete[] array;
        array = newarray;
    }

    void append(int value){
        if(length >= capacity){
            try{
                resize();
            }catch(...){
                throw "Failed to append";
            }
        }
        *(array+length) = value;
        length += 1;
        return;
    }

    void print(){
        for(int i=0; i<length; i++){
            cout<<*(array+i)<<" ";
        }
    }

    int pop(){
        length -= 1;
        return *(array+length);
    }

    int getCapacity(){
        return capacity;
    }

    int getSize(){
        return length;
    }

    ~Array(){
        delete[] array;
    }
};

int main(){
    Array arr;
    arr.append(1);
    arr.append(2);
    arr.append(3);
    arr.append(4);
    arr.append(5);
    arr.append(6);
    arr.append(7);
    arr.print();
    cout<<arr.getCapacity()<<" "<<arr.getSize()<<endl;
    cout<<arr.pop()<<endl;
    arr.print();
    return 0;
}