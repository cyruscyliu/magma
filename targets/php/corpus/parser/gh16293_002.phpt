<?php

assert_options(ASSERT_EXCEPTION, 0);
assert_options(ASSERT_BAIL, 1);
assert_options(ASSERT_CALLBACK, function () {
    throw new Exception('Boo');
});
assert(false);

?>