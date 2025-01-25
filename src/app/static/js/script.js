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
});
