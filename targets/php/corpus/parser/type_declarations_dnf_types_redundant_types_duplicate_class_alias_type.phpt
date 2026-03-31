<?php

interface X {}

use A as B;
function foo(): (X&A)|(X&B) {}

?>