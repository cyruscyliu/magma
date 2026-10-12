<?php

@assert_options(ASSERT_EXCEPTION, 0);
@assert_options(ASSERT_BAIL, 1);
@assert_options(ASSERT_CALLBACK, 'f1');
assert(false);

?>