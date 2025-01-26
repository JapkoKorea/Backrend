document.addEventListener("DOMContentLoaded", () => {
    const authButton = document.getElementById("auth-button");
    console.log(authButton)
    if (authButton) {
        const kakaoAccessToken = document.cookie
            .split("; ")
            .find(row => row.startsWith("kakao_access_token="))
            ?.split("=")[1];
        const userName = document.cookie
            .split("; ")
            .find(row => row.startsWith("user_name="))
            ?.split("=")[1];

        if (kakaoAccessToken) {
            // 로그아웃 버튼으로 변경
            authButton.textContent = decodeURIComponent(userName || "사용자");  // 디코딩된 사용자 이름 사용
            authButton.onclick = async () => {
                console.log("Sending Kakao Access Token:", kakaoAccessToken); // 디버깅용 로그
                try {
                    const response = await fetch(`/kakao/logout?kakao_access_token=${kakaoAccessToken}`, {
                        method: "GET",
                    });

                    if (response.ok) {
                        alert("로그아웃 성공!");
                        document.cookie = "kakao_access_token=; Max-Age=0"; // 쿠키 삭제
                        document.cookie = "user_name=; Max-Age=0"; // 쿠키 삭제
                        window.location.reload();
                    } else {
                        alert("로그아웃 실패. 다시 시도해주세요.");
                    }
                } catch (error) {
                    console.error("Error logging out:", error);
                }
            };
        } else {
            // 로그인 버튼으로 변경
            authButton.textContent = "로그인";
            authButton.onclick = () => {
                window.location.href = "/kakao/login"; // 카카오 로그인 호출
            };
        }
    }
    const images = document.querySelectorAll("img");

    images.forEach(image => {
        image.addEventListener("click", async (event) => {
            const imageId = event.target.getAttribute("data-id");
            const imageName = event.target.getAttribute("data-name");
            const timestamp = Date.now();

            const payload = {
                image_id: imageId,
                image_name: imageName,
                timestamp: timestamp,
            };

            console.log("Payload:", payload); // 디버깅용 로그
            // 쿠키에서 Access Token 가져오기
            const accessToken = document.cookie
                .split("; ")
                .find(row => row.startsWith("access_token="))
                ?.split("=")[1];
            try {
                const response = await fetch("/click", { // '/' 경로 확인 필요
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${accessToken}`, // 토큰 포함
                    },
                    body: JSON.stringify(payload),
                });

                const result = await response.json();
                console.log("클릭 로그 결과:", result);
            } catch (error) {
                console.error("Error logging click:", error);
            }
        });
    });
});
