const assert=require("node:assert/strict");
const {calculate,readValues}=require("../landing/assets/calculators.js");
const cases=[["daily",{"balance":30000,"bills":10000,"save":5000,"days":10},1500],["daily",{"balance":10,"bills":20,"save":0,"days":1},10],["purchase",{"balance":35000,"bills":12000,"living":10000,"save":5000,"price":6000},2000],["month",{"income":90000,"bills":35000,"living":25000,"save":15000},15000],["payday",{"income":50000,"bills":18000,"save":10000,"days":15},1466],["savings",{"target":150000,"start":30000,"months":12},10000],["cushion",{"essential":60000,"months":3,"start":20000},180000],["family",{"first":80000,"second":120000,"bills":90000},36000],["move",{"rent":45000,"deposit":45000,"transport":12000,"setup":15000,"reserve":20000,"start":50000},137000],["deadline",{"target":100000,"start":40000,"monthly":10000},6],["debt",{"income":100000,"bills":25000,"living":40000},25]];
for(const [kind,v,expected] of cases){assert.equal(Number(calculate(kind,v).value.replace(/[^\d]/g,"")),expected,kind)}
assert.equal(calculate("deadline",{target:10,start:0,monthly:0}).value,"—");
assert.equal(calculate("family",{first:0,second:0,bills:5}).value,"—");
assert.equal(calculate("savings",{target:10,start:20,months:2}).value,"0 ₽");
assert.equal(readValues({querySelectorAll:()=>[{validity:{valid:false},valueAsNumber:NaN}]}),null);
assert.equal(readValues({querySelectorAll:()=>[{validity:{valid:true},valueAsNumber:0,dataset:{field:"start"}}]}).start,0);
console.log("Calculator arithmetic and validation: OK");
