<?php

#[\Deprecated]
function test1() {
}

#[\Deprecated()]
function test2() {
}

#[\Deprecated("use test() instead")]
function test3() {
}

#[\Deprecated(message: "use test() instead", since: "1.0")]
function test4() {
}

#[\Deprecated(since: "1.0", message: "use test() instead")]
function test5() {
}

#[\Deprecated(since: "1.0")]
function test6() {
}

test1();
test2();
test3();
test4();
test5();
test6();

?>