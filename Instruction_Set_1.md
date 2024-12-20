```c
1	('s' to switch to tier_1.txt session 1){

	1	(string_var# assignment){
		
		0	Command set = {(0), ... (13106)}
		1	[string_var0](0) = <f1 = open("hello-world.txt","w")>
		2	[string_var1](1) = <f1.write("Hello World, this is Dominic Alexander Cooper. Welcome to Data Architectural Command")>
		3	[string_var2](2) = <f1.close()>
		4	[string_var3](3) = <f2 = open(string_var5, string_var6)>
		5	[string_var4](4) = <value>
		6	[string_var5](5) = <value>
		7	[string_var6](6) = <value>
		8	[string_var7](7) = <value>
		9	[string_var8](8) = <value>
		10	[string_var9](9) = <f3 = open(string_var8, string_var6).writelines([string_var5 if i == string_var7 else line for i, line in enumerate(open(string_var8))])>
		11	[string_var10](10) = <f2.close()>
		12	[string_var11](11) = <f2.write(string_var12)>
		13	[string_var12](12) = <value>
		14	[string_var13](13) = <value>

	}

	2	(var_given# assignment){

		0	Command set = {(13107), ... (26213)}
		1	[var_given0](13107) = <string_var0>
		2	[var_given1](13108) = <string_var1>
		3	[var_given2](13109) = <string_var2>
		4	[var_given3](13110) = <string_var3>
		5	[var_given4](13111) = <string_var4>
		6	[var_given5](13112) = <string_var5>
		7	[var_given6](13113) = <string_var6>
		8	[var_given7](13114) = <string_var7>
		9	[var_given8](13115) = <string_var8>
		10	[var_given9](13116) = <string_var9>
		11	[var_given10](13117) = <string_var10>
		12	[var_given11](13118) = <string_var11>
		13	[var_given12](13119) = <string_var12>
		14	[var_given13](13120) = <string_var13>

	}

	3	(var_glob# automatic assignment){

		0	Command set = {(26214), ... (39320)}
		1	[var_glob0](26214) is equal to var_given0
		2	[var_glob1](26215) is equal to var_given1
		3	[var_glob2](26216) is equal to var_given2
		4	[var_glob3](26217) is equal to var_given3
		5	[var_glob4](26218) is equal to var_given4
		6	[var_glob5](26219) is equal to var_given5
		7	[var_glob6](26220) is equal to var_given6
		8	[var_glob7](26221) is equal to var_given7
		9	[var_glob8](26222) is equal to var_given8
		10	[var_glob9](26223) is equal to var_given9
		11	[var_glob10](26224) is equal to var_given10
		12	[var_glob11](26225) is equal to var_given11
		13	[var_glob12](26226) is equal to var_given12
		14	[var_glob13](26227) is equal to var_given13

	}

	4	(exec(var_glob#) code line execution){

		0	Command set = {(39321), ... (52427)}
		1	[eval(var_glob0)](39321) to be executed
		2	[exec(var_glob1)](39322) to be executed
		3	[exec(var_glob2)](39323) to be executed
		4	[exec(var_glob3)](39324) to be executed
		5	[exec(var_glob4)](39325) to be executed
		6	[exec(var_glob5)](39326) to be executed
		7	[exec(var_glob6)](39327) to be executed
		8	[exec(var_glob7)](39328) to be executed
		9	[exec(var_glob8)](39329) to be executed
		10	[exec(var_glob9)](39330) to be executed
		11	[exec(var_glob10)](39331) to be executed
		12	[exec(var_glob11)](39332) to be executed
		13	[exec(var_glob12)](39333) to be executed
		14	[exec(var_glob13)](39334) to be executed

	}

	5	(eval(var_glob#) code line evaluation){

		0	Command set = {(52428), ... (65534)}

	}
	
	6	(Bonus Command){
	
		0	Command Set = {(65535)}
	
	}
	
	7	(Command Types){
	
		1	write
		2	read
	
	}
	
	8	(Command Sequence cs1: Writ to a file){
	
		1	(0 13107 26214 39321)
		2	inputs of 1.8.1:
			<input string_var0 value>,
			<input "string_var0" for var_given0>,
			input remaining commands by id
		3	(1 13108 26215 39322)
		4	inputs of 1.8.3:
			<input string_var1 value>,
			<input "string_var1" for var_given1>,
			input remaining commands by id
		5	(2 13109 26216 39323)
		6	inputs of 1.8.5:
			<input string_var2 value>,
			<input "string_var2" for var_given2>,
			input remaining commands by id
		7	helloWorld_program{1.8.1, 1.8.3, 1.8.5} with descriptions {1.8.2, 1.8.4, 1.8.6}
	
	}

	9	(Command Sequence cs2: Write to a file (Dynamic)){

		1	(5 13112 26219)
		2	inputs of 1.9.1:
			<input string_var5 value>,
			<input "string_var5" for var_given5>,
			input remaining commands by id
		3	(6 13113 26220)
		4	inputs of 1.9.3:
			<input string_var6 value>,
			<input "string_var6" for var_given6>,
			input remaining commands by id
		5	(12 13119 26226)
		6	inputs of 1.9.5:
			<input string_var12 value>,
			<input "string_var12" for var_given12>,
			input remaining commands by id
		7	(3 13110 26217 39324)
		8	inputs of 1.9.7:
			<input string_var3 value>,
			<input "string_var3" for var_given3>,
			input remaining commands by id
		9	(11 13118 26225 39332)
		10	inputs of 1.9.9:
			<input string_var11 value>,
			<input "string_var11" for var_given11>,
			input remaining commands by id
		11	(10 13117 26224 39331)
		12	inputs of 1.9.11:
			<input string_var10 value>,
			<input "string_var10" for var_given10>,
			input remaining commands by id
		13	file-writing program{1.9.1, 1.9.3, 1.9.5, 1.9.7, 1.9.9, 1.9.11} with 1.9.14
		14	description{1.9.2, 1.9.4, 1.9.6, 1.9.8, 1.9.10, 1.9.12}

	}

	10	(Command Sequence cs3: General Code File execution (Dynamic)){

		1	loop 1.9.13 until complete then 1.10.2 with 1.10.3
		2	13 13120 26227 39334
		3	inputs of 1.10.2:
			<input string_var13 value>,
			<input "string_var13" for var_given13>,
			input remaining commands by id

	}

}
```