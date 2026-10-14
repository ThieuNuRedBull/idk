#include <bits/stdc++.h>
#define ll long long
using namespace std;
struct Node{
    Node *left,*right;
    ll data;
    Node(ll val){
        data=val;
        left=right=NULL;
    }
};
ll totalLeaf;
// Node* insert(Node *root,ll val, char c){
//     if(root==NULL) return new Node(val);
//     if(c=='L') root->left=insert(root->left,val,c);
//     else root->right=insert(root->right,val,c);
//     return root;
// }
void duyet(Node *root){
    deque<Node*> q;
    q.push_back(root);
    ll i=0;
    while(!q.empty()){
        Node *tmp;
        if(i%2==0){
            *tmp=q.front();
        }else {
            *tmp=q.back();
        }
        q.pop_front();
        cout<<tmp->data<<" ";
        if(i%2==0){
            if(tmp->left) q.push_back(tmp->left);
            if(tmp->right) q.push_back(tmp->right);
        }else{
            if(tmp->right) q.push_front(tmp->right);
            if(tmp->left) q.push_front(tmp->left);
        }
        i++;
    }
}
int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    ll t;
    cin>>t;
    while(t--){
        Node *root=NULL;
        ll n;
        cin>>n;
        totalLeaf=0;
        map<ll,Node*> mp;
        for(ll i=0;i<n;i++){
            ll x,y;
            char c;
            cin>>x>>y>>c;
            if(root==NULL){
                root=new Node(x);
                mp[x]=root;
            }
            if(mp.count(y)==0){
                mp[y]=new Node(y);
            }
            if(c=='L') mp[x]->left=mp[y];
            else mp[x]->right=mp[y];
        }
        duyet(root);
        cout<<"\n";
    }
}
/*
        40
    30      80
        35      100

*/
