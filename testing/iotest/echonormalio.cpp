#include <cstdio>

using namespace std;

int n;
char buf[256];

int main(){
    scanf("%d", &n);

    while(n--){
        scanf("%s", &buf);
        printf("%s\n", buf);
    }
}