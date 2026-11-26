"use strict";
function calculate(kind,v){
 const money=(n)=>Math.round(n).toLocaleString("ru-RU")+" ₽";
 const result=(label,n,detail)=>({label,value:money(n),detail});
 const free=v.balance-v.bills-v.save;
 switch(kind){
 case "daily":return free<0?result("Дефицит до зарплаты",-free,"Свободных денег нет по введенному плану."):result("Ориентир в день",Math.floor(free/v.days),"На весь период: "+money(free)+".");
 case "purchase":{const rest=v.balance-v.bills-v.living-v.save-v.price;return rest<0?result("Не хватает по плану",-rest,"Покупка потребует изменить план."):result("Останется после покупки",rest,"Обязательства, жизнь и накопления учтены.");}
 case "month":{const rest=v.income-v.bills-v.living-v.save;return rest<0?result("Дефицит месяца",-rest,"План превышает доход."):result("Свободный остаток",rest,"После всех указанных расходов и накоплений.");}
 case "payday":{const rest=v.income-v.bills-v.save;return rest<0?result("Дефицит получки",-rest,"Обязательства и взнос превышают доход."):result("На каждый день",Math.floor(rest/v.days),"На жизнь до следующей выплаты: "+money(rest)+".");}
 case "savings":return result("Взнос в месяц",Math.ceil(Math.max(0,v.target-v.start)/v.months),"Осталось накопить: "+money(Math.max(0,v.target-v.start))+".");
 case "cushion":return result("Размер резерва",v.essential*v.months,"Осталось собрать: "+money(Math.max(0,v.essential*v.months-v.start))+".");
 case "family":{const total=v.first+v.second;if(total===0)return {label:"Уточните доход",value:"—",detail:"При нулевом общем доходе пропорция не определяется."};const first=Math.round(v.bills*v.first/total);return result("Взнос первого партнера",first,"Взнос второго: "+money(v.bills-first)+". Поровну: "+(v.bills/2).toLocaleString("ru-RU",{maximumFractionDigits:2})+" ₽ каждому."+(v.bills>total?" Общие расходы выше доходов на "+money(v.bills-total)+".":""));}
 case "move":{const total=v.rent+v.deposit+v.transport+v.setup+v.reserve;return result("Нужно на старт",total,"Осталось накопить: "+money(Math.max(0,total-v.start))+".");}
 case "deadline":{const rest=Math.max(0,v.target-v.start);if(rest===0)return {label:"Цель уже собрана",value:"0 мес.",detail:"Дополнительные взносы не нужны при неизменной цене."};if(v.monthly===0)return {label:"Срок не определяется",value:"—",detail:"Укажите положительный ежемесячный взнос."};return {label:"До цели",value:Math.ceil(rest/v.monthly).toLocaleString("ru-RU")+" мес.",detail:"Осталось накопить: "+money(rest)+"."};}
 case "debt":{if(v.income<=0)return {label:"Уточните доход",value:"—",detail:"Для расчета нужен положительный доход."};const pct=(v.bills/v.income*100).toLocaleString("ru-RU",{maximumFractionDigits:1});const rest=v.income-v.bills-v.living;return {label:"Доля платежей в доходе",value:pct+"%",detail:rest<0?"После необходимых расходов дефицит "+money(-rest)+".":"После платежей и необходимых расходов: "+money(rest)+"."};}
 default:throw Error("unknown calculator");
 }
}
function readValues(form){const values={};for(const el of form.querySelectorAll("input[data-field]")){const value=el.valueAsNumber;if(!el.validity.valid||!Number.isFinite(value)||value<0||value>1000000000)return null;values[el.dataset.field]=value;}return values;}
if(typeof module!=="undefined")module.exports={calculate,readValues};
if(typeof document!=="undefined")document.querySelectorAll("[data-kb-calculator]").forEach(form=>{const render=()=>{const values=readValues(form);const out=form.querySelector(".kb-result");const r=values?calculate(form.dataset.kbCalculator,values):{label:"Проверьте значения",value:"—",detail:"Заполните все поля допустимыми неотрицательными числами."};out.querySelector("span").textContent=r.label;out.querySelector("strong").textContent=r.value;out.querySelector("small").textContent=r.detail;};form.addEventListener("input",render);render();});
