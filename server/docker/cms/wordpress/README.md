```shell
# generatedpress theme add postviews; install WP-PostViews plugin
vim wp-content/themes/generatepress/inc/structure/post-meta.php
add it in 230 line
if(function_exists('the_views')) { the_views(); }
```