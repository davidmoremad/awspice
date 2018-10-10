
###################
# 		SERVICES		#
###################

service_file="source/awspice-services.rst"

# 1. Get files in 'services' folder
printf "\nServices\n========\n\n" > $service_file
ls -1 ../awspice/services/ | grep '[a-z0-9].py$' | grep -v base.py | while read -r file ;
do
	# 2. Get Class of the file
	cat ../awspice/services/$file | grep '^class\s[a-zA-Z0-1]' | awk '{print $2}' | cut -d '(' -f1 | cut -d ':' -f1 | while read -r class ;
	do
		# 3. Get Methods of the Class
		filename=$(echo $file | cut -d '.' -f1) 										 				 # ec2.py -> ec2
		service_title=$(echo $class | sed 's/\Service//g')
		# service_title=$(echo $class | sed 's/\Service//g' | awk '{print toupper($0)}')  # Service title UPPERCASE
		methods=$(cat ../awspice/services/$file | grep "def [a-zA-Z]" | awk '{print $2}' | cut -d '(' -f1 | perl -ne 'print "   awspice.services.'$filename'.'$class'.$_"')


		printf "\n\n\n$service_title\n" >>  $service_file
		printf %${#service_title}s |tr " " "-" >>  $service_file
		printf "\n\n.. autosummary::\n\n" >>  $service_file
		echo "$methods" >>  $service_file
	done
done


###################
# 		MODULES 		#
###################

module_file="source/awspice-modules.rst"

# 1. Get files in 'services' folder
printf "\nModules\n========\n\n" > $module_file
ls -1 ../awspice/modules/ | grep '[a-z0-9].py$' | grep -v base.py | while read -r file ;
do
	# 2. Get Class of the file
	cat ../awspice/modules/$file | grep '^class\s[a-zA-Z0-1]' | awk '{print $2}' | cut -d '(' -f1 | cut -d ':' -f1 | while read -r class ;
	do
		# 3. Get Methods of the Class
		filename=$(echo $file | cut -d '.' -f1) 										 				 # ec2.py -> ec2
		module_title=$(echo $class | sed 's/\Module//g')
		# service_title=$(echo $class | sed 's/\Service//g' | awk '{print toupper($0)}')  # Service title UPPERCASE
		methods=$(cat ../awspice/modules/$file | grep "def [a-zA-Z]" | awk '{print $2}' | cut -d '(' -f1 | perl -ne 'print "   awspice.modules.'$filename'.'$class'.$_"')


		printf "\n\n\n$module_title\n" >>  $module_file
		printf %${#module_title}s |tr " " "-" >>  $module_file
		printf "\n\n.. autosummary::\n\n" >>  $module_file
		echo "$methods" >>  $module_file
	done
done
