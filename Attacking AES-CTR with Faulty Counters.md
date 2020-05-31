**Attacking AES-CTR with Faulty Counters:**

There are several properties of AES in CTR mode that make it vulnerable to attacks. Since successive blocks of plaintext are independently encrypted using a key and a counter, causing counter collisions allows attackers to compute cipher text collisions. These attacks take advantage of the associativity of XOR, i.e. $(A+B=C) \Rightarrow (A=B+C) \Rightarrow (B=C+A)$. Suppose we have two arbitrary plaintext blocks $X, Y$ and let $ctr_i$ at state $i$. We denote the encryption of some input $B$ under a given key $K$ as $E_k(B)$. Let $+$ denote XOR:
$$
X' = E_k(ctr_i) + X \\
Y' = E_k(ctr_i) + Y
$$
Here, $X', Y'$ represent the cipher-text blocks produced by xoring the plain text blocks $X, Y$ with the output produced from encrypting the counter at state $i$ under the key $K$. By the associativity of XOR, we can see that a collision of counter produces the following equality:
$$
E_k(ctr_i) = X' + X \\
E_k(ctr_i) = Y' + Y \\
Y' + Y = X' + X \\
$$
Thus if any part of $X$ is known, then $X'$ is also known, by taking the XOR of the cipher text ($E_k(ctr_i)$) and down portion of X. 



**Using Known Length and Poorly Initialized Counters**

If counters are not properly initialized, chosen plaintext attacks can be used to reveal information about encrypted messages. Consider  a piece of plaintext "Hello world". If counters do not take into account some random seed to change values each time a communication session is initialized, it becomes easy to predict the value of the counter, especially after the counter is first initialized. This can be used to create counter collisions, and allow us to access information about plaintext.
$$
X' = E_k(ctr_i) + X
$$




