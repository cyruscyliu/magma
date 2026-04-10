<?php

class ThisClassDoesExist { }

const Closure = ThisClassDoesExist::thisMethodDoesNotExist(...);

var_dump(Closure);

?>