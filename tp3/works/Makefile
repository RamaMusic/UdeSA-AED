local:
	gcc -g -std=c99 -Wall -Wconversion -Wno-sign-conversion -Werror -Wl,--wrap=malloc -o tp3 *.c
	valgrind -s --error-exitcode=1 --leak-check=full --show-leak-kinds=all --track-origins=yes ./tp3
	rm tp3

docker:
	docker build --tag udesa_tp3 .
	docker run udesa_tp3

clean_docker:
	docker rmi -f $(docker images | grep udesa_tp3 | tr -s ' ' | cut -d ' ' -f 3)
