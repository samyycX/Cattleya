<template>
  <div class="block w-full bg-theme-0 h-max">
    <div class="w-7/12 px-12 pt-7 mx-auto max-w-none prose prose-cattleya prose-xl text-left bg-theme-0 h-max">
      <BlogMdxRender :content="mdx" />  
    </div>
  </div>
</template>

<script setup lang="jsx">
import BlogMdxRender from '@/components/blog/BlogMdxRender.vue';

import { ref } from 'vue';

const mdx = ref(`

# Heading (rank 1)
## Heading 2
### 3
#### 4
##### 5
###### 6

Foot只支持Sixel，不支持Kitty和iTerm的图片协议。在fastfetch中设置type为Sixel时，图片的透明度会失效。经过大量的冲浪，我找到了一个解决方案

> Block quote

* Unordered
* List

1. Ordered
2. List

A paragraph, introducing a thematic break:

---

~~~js
some.code()
function
~~~

| THead1          |      THead2       |           THead3 |
| :-------------- | :---------------: | ---------------: |
| text-align:left | text-align:center | text-align:right |

$$\\LaTeX$$
`)

</script>

<style scoped>

h1 {

}
</style>
